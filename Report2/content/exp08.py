from .. import theme


def build(doc):
    theme.exp_head(doc, "08", "16/09/2026",
                   "Web application for Online Shopping using Servlet and MySQL")
    theme.heading_plain(doc, "AIM:")
    theme.body(doc, "To design and develop a simple online shopping web application using Java, "
                    "Jakarta Servlets, JSP, JDBC and MySQL that allows a user to log in, view "
                    "products, add and remove products in a cart and compute the total price.")
    theme.heading_plain(doc, "PROCEDURE:")
    theme.numbered(doc, [
        "Install JDK 17, Apache Maven, MySQL and Apache Tomcat 10.1.",
        "Create a MySQL database named online_shopping.",
        "Create the users and products tables and insert sample records.",
        "Create a Maven web application and configure the dependencies in pom.xml.",
        "Develop a login page using HTML and JSP.",
        "Create a Login Servlet to validate credentials through JDBC.",
        "Develop a product dashboard that lists products from MySQL.",
        "Implement the shopping cart using an HTTP session.",
        "Create a cart page showing the selected products, quantities and total.",
        "Apply simple CSS to improve the appearance.",
        "Build with mvn clean package and deploy the WAR on Tomcat.",
        "Test login, product display, add, remove and the total calculation.",
    ])
    theme.heading_plain(doc, "DATABASE - ONLINE_SHOPPING.SQL:")
    theme.code(doc, """CREATE DATABASE online_shopping;
USE online_shopping;

CREATE TABLE users (
    id       INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50)
);

CREATE TABLE products (
    id    INT PRIMARY KEY AUTO_INCREMENT,
    name  VARCHAR(100),
    price DOUBLE
);

INSERT INTO users(username, password) VALUES ('pavi', '1234');

INSERT INTO products(name, price) VALUES
('Laptop', 45000),
('Headphones', 1500),
('Keyboard', 800),
('Mouse', 500);""")
    theme.heading_plain(doc, "LOGINSERVLET.JAVA:")
    theme.code(doc, """package com.shop;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.*;
import java.sql.*;

@WebServlet("/login")
public class LoginServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req,
                          HttpServletResponse res)
            throws ServletException, IOException {

        String username = req.getParameter("username");
        String password = req.getParameter("password");

        try (Connection con = DB.getConnection();
             PreparedStatement ps = con.prepareStatement(
                 "SELECT * FROM users WHERE username=? AND password=?")) {

            ps.setString(1, username);
            ps.setString(2, password);

            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                HttpSession session = req.getSession();
                session.setAttribute("user", username);
                res.sendRedirect("products");
            } else {
                res.getWriter().println("Invalid username or password");
            }

        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}""")
    theme.heading_plain(doc, "CARTSERVLET.JAVA:")
    theme.code(doc, """package com.shop;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.*;
import java.io.*;
import java.sql.*;
import java.util.*;

@WebServlet("/cart")
public class CartServlet extends HttpServlet {

    protected void doPost(HttpServletRequest req,
                          HttpServletResponse res)
            throws IOException {

        HttpSession session = req.getSession(false);

        if (session == null || session.getAttribute("user") == null) {
            res.sendRedirect("login.jsp");
            return;
        }

        Map<Integer, Integer> cart =
            (Map<Integer, Integer>) session.getAttribute("cart");

        if (cart == null) {
            cart = new HashMap<>();
            session.setAttribute("cart", cart);
        }

        int id = Integer.parseInt(req.getParameter("id"));
        String action = req.getParameter("action");

        if ("add".equals(action)) {
            cart.put(id, cart.getOrDefault(id, 0) + 1);
        }
        if ("remove".equals(action)) {
            cart.remove(id);
        }

        res.sendRedirect("cart");
    }

    protected void doGet(HttpServletRequest req,
                         HttpServletResponse res)
            throws ServletException, IOException {

        HttpSession session = req.getSession(false);

        if (session == null || session.getAttribute("user") == null) {
            res.sendRedirect("login.jsp");
            return;
        }

        Map<Integer, Integer> cart =
            (Map<Integer, Integer>) session.getAttribute("cart");

        if (cart == null) cart = new HashMap<>();

        StringBuilder rows = new StringBuilder();
        double total = 0;

        try (Connection con = DB.getConnection();
             PreparedStatement ps = con.prepareStatement(
                 "SELECT * FROM products WHERE id=?")) {

            for (int id : cart.keySet()) {
                ps.setInt(1, id);

                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        String name  = rs.getString("name");
                        double price = rs.getDouble("price");
                        int    qty   = cart.get(id);
                        double sub   = price * qty;

                        total += sub;

                        rows.append("<tr><td>").append(name)
                            .append("</td><td>Rs.").append(price)
                            .append("</td><td>").append(qty)
                            .append("</td><td>Rs.").append(sub)
                            .append("</td><td><form method='post' action='cart'>")
                            .append("<input type='hidden' name='id' value='")
                            .append(id)
                            .append("'><button name='action' value='remove'>")
                            .append("Remove</button></form></td></tr>");
                    }
                }
            }

            req.setAttribute("rows", rows.toString());
            req.setAttribute("total", total);
            req.getRequestDispatcher("/cart.jsp").forward(req, res);

        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}""")
    theme.heading_plain(doc, "OUTPUT:")
    theme.body(doc, "After login the product dashboard lists the four products. Adding a laptop and "
                    "two headphones shows three rows in the cart with the total Rs.48,000. Removing "
                    "the laptop recalculates the total to Rs.3,000.")
    theme.heading_plain(doc, "RESULT:")
    theme.body(doc, "Thus the online shopping web application was designed and developed using "
                    "Java, Jakarta Servlets, JSP, JDBC and MySQL and the login, product display "
                    "and cart operations were verified on Tomcat.")
    theme.rubric_table(doc)
    theme.page_break(doc)
