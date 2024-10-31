package com.dimas;

public class Util {
    public static void setSystemProperty(String s) {
        String[] parts = s.split("=");

        if (parts.length == 2) {
            String key = parts[0].trim();
            String value = parts[1].trim();

            System.setProperty(key, value);
        } else {
            throw new IllegalArgumentException("Invalid input format. Expected key=value.");
        }
    }
}
