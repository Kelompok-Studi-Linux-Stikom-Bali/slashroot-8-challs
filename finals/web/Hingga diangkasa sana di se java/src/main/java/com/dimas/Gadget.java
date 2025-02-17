package com.dimas;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;

public class Gadget implements Serializable {

    private Runnable command;

    public Gadget(Command command) {
        this.command = command;
    }

    private final void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        String deserialized = System.getProperty("deserialized");
        if (deserialized != null && !deserialized.isEmpty()) {
            in.defaultReadObject();
            command.run();
        }
    }
}
