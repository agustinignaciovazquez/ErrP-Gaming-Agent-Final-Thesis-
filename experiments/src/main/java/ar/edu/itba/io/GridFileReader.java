package ar.edu.itba.io;

import java.awt.*;
import java.awt.geom.Point2D;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class GridFileReader {
    private Point dimesions;
    private final ArrayList<Point> positions;
    private int index = 0;
    private int gamesLoaded = 0;

    public GridFileReader(String filename) throws IOException {
        this.positions = new ArrayList<>();
        readGame(filename);
    }
    private void readGame(String filename) throws IOException {
        try(BufferedReader bufferedReader = new BufferedReader(new FileReader(filename))) {
            String line = bufferedReader.readLine();
            this.dimesions = parseDimensions(line);

            Point p;
            do {
                p = readPosition(bufferedReader);
                this.positions.add(p);
            }while (p != null);
        } finally {
            gamesLoaded++;
        }
    }
    public void addNewGame(String filename) throws IOException {
        readGame(filename);
    }

    public int getGamesLoaded() {
        return gamesLoaded;
    }

    public Point getNextPosition(){
        return positions.get(index++);
    }

    public Point getDimesions(){
        return dimesions;
    }

    private Point readPosition(BufferedReader br) throws IOException {
        String line = br.readLine();
        if(line == null)
            return null;
        //Avoid empty lines
        if(line.isEmpty())
            return readPosition(br);

        return parsePosition(line);
    }

    private Point parsePosition(String line) throws IOException {
        String[] splited = line.split("-");
        if (splited.length != 2)
            throw new IOException();

        int x = Integer.parseInt(splited[0]);
        int y = Integer.parseInt(splited[1]);
        return new Point(x,y);
    }

    private Point parseDimensions(String line) throws IOException {
        String[] splited = line.split("x");
        if (splited.length != 2)
            throw new IOException();

        int x = Integer.parseInt(splited[0]);
        int y = Integer.parseInt(splited[1]);
        return new Point(x,y);
    }
}
