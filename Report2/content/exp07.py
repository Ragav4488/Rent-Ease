from .. import theme


def build(doc):
    theme.exp_head(doc, "07", "02/09/2026",
                   "Web application for leave management using Servlet and MySQL")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design a leave management web application using Jakarta Servlets, JSP, "
                    "JDBC and MySQL in which an employee applies for leave, a manager approves or "
                    "rejects it, and the leave balance is maintained.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Install JDK 17, Apache Maven, MySQL and Apache Tomcat 10.1.",
        "Create the database leave_management with employee and leave_request tables.",
        "Create a Maven web project and add the Jakarta Servlet and MySQL connector dependencies.",
        "Write DB.java to return a JDBC connection from DriverManager.",
        "Build login.jsp and a LoginServlet that stores the employee id in the session.",
        "Build apply.jsp and an ApplyLeaveServlet that validates and inserts a leave request.",
        "Add an AuthFilter that blocks protected URLs when no session exists.",
        "Build ListLeaveServlet to show the signed-in employee's requests.",
        "Build ApproveLeaveServlet so a manager can approve or reject a pending request.",
        "Deduct the approved days from the leave balance inside a transaction.",
        "Package with mvn clean package, deploy the WAR on Tomcat and test every workflow.",
    ])
    theme.heading_plain(doc, "POM.XML:")
    theme.code(doc, """<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.leave</groupId>
    <artifactId>leave-management</artifactId>
    <version>1.0</version>
    <packaging>war</packaging>

    <properties>
        <maven.compiler.release>17</maven.compiler.release>
    </properties>

    <dependencies>
        <dependency>
            <groupId>jakarta.servlet</groupId>
            <artifactId>jakarta.servlet-api</artifactId>
            <version>6.0.0</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <version>9.4.0</version>
        </dependency>
    </dependencies>

    <build>
        <finalName>leave-management</finalName>
    </build>
</project>""")
    theme.heading_plain(doc, "DATABASE - LEAVE_MANAGEMENT.SQL:")
    theme.code(doc, """CREATE DATABASE leave_management;
USE leave_management;

CREATE TABLE employees (
    emp_id   INT PRIMARY KEY AUTO_INCREMENT,
    name     VARCHAR(80)  NOT NULL,
    email    VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role     ENUM('employee','manager') DEFAULT 'employee',
    balance  INT DEFAULT 20
);

CREATE TABLE leave_requests (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    emp_id     INT NOT NULL,
    leave_type ENUM('Casual','Sick','Earned') NOT NULL,
    from_date  DATE NOT NULL,
    to_date    DATE NOT NULL,
    days       INT  NOT NULL,
    reason     VARCHAR(255),
    status     ENUM('pending','approved','rejected') DEFAULT 'pending',
    applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

INSERT INTO employees (name, email, password, role, balance)
VALUES ('Pavi', 'pavi@org.in', '1234', 'employee', 20),
       ('Ravi', 'ravi@org.in', '1234', 'manager', 20);""")
    theme.heading_plain(doc, "APPLYLEAVESERVLET.JAVA:")
    theme.code(doc, """package com.leave;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.*;
import java.sql.*;
import java.time.*;
import java.time.temporal.ChronoUnit;

@WebServlet("/apply")
public class ApplyLeaveServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req,
                          HttpServletResponse res)
            throws ServletException, IOException {

        HttpSession session = req.getSession(false);
        if (session == null || session.getAttribute("empId") == null) {
            res.sendRedirect("login.jsp");
            return;
        }

        int empId      = (Integer) session.getAttribute("empId");
        String type    = req.getParameter("leave_type");
        LocalDate from = LocalDate.parse(req.getParameter("from_date"));
        LocalDate to   = LocalDate.parse(req.getParameter("to_date"));
        String reason  = req.getParameter("reason");

        if (to.isBefore(from)) {
            res.getWriter().println("End date must be after the start date.");
            return;
        }

        long days = ChronoUnit.DAYS.between(from, to) + 1;

        try (Connection con = DB.getConnection();
             PreparedStatement ps = con.prepareStatement(
                 "INSERT INTO leave_requests " +
                 "(emp_id, leave_type, from_date, to_date, days, reason) " +
                 "VALUES (?,?,?,?,?,?)")) {

            ps.setInt(1, empId);
            ps.setString(2, type);
            ps.setDate(3, Date.valueOf(from));
            ps.setDate(4, Date.valueOf(to));
            ps.setLong(5, days);
            ps.setString(6, reason);
            ps.executeUpdate();

            res.sendRedirect("list");

        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}""")
    theme.heading_plain(doc, "APPROVELEAVESERVLET.JAVA:")
    theme.code(doc, """package com.leave;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.*;
import java.sql.*;

@WebServlet("/approve")
public class ApproveLeaveServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req,
                          HttpServletResponse res)
            throws ServletException, IOException {

        int requestId = Integer.parseInt(req.getParameter("request_id"));
        String action = req.getParameter("action");   // approve | reject

        try (Connection con = DB.getConnection()) {
            con.setAutoCommit(false);

            try {
                PreparedStatement sel = con.prepareStatement(
                    "SELECT emp_id, days FROM leave_requests " +
                    "WHERE request_id = ? AND status = 'pending'");
                sel.setInt(1, requestId);
                ResultSet rs = sel.executeQuery();

                if (rs.next()) {
                    int empId = rs.getInt("emp_id");
                    int days  = rs.getInt("days");

                    con.prepareStatement(
                        "UPDATE leave_requests SET status = '" +
                        ("approve".equals(action) ? "approved" : "rejected") +
                        "' WHERE request_id = " + requestId
                    ).executeUpdate();

                    if ("approve".equals(action)) {
                        PreparedStatement bal = con.prepareStatement(
                            "UPDATE employees SET balance = balance - ? " +
                            "WHERE emp_id = ?");
                        bal.setInt(1, days);
                        bal.setInt(2, empId);
                        bal.executeUpdate();
                    }
                }

                con.commit();
            } catch (Exception e) {
                con.rollback();
                throw e;
            }

            res.sendRedirect("list");

        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "The employee logs in, applies for three days of casual leave and the request "
                    "appears as Pending. The manager approves it, the status becomes Approved and "
                    "the employee's balance drops from 20 to 17.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the leave management web application was developed using Jakarta "
                    "Servlets, JSP, JDBC and MySQL and the apply and approve workflows were "
                    "verified on Tomcat.")
    theme.rubric_table(doc)
    theme.page_break(doc)
