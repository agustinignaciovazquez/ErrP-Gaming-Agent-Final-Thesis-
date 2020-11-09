package ar.edu.itba.io;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class GridLightsFileRotator {

  private static final int AVOIDABLE_LINES = 1;

  public static void rotate(final String oldFilename, final List<String> newFilenames) throws IOException {
    final List<FileWriter> fws = new ArrayList<>();
    newFilenames.forEach(fw -> {
      try {
        fws.add(new FileWriter(fw));
      } catch (IOException e) {
        e.printStackTrace();
      }
    });
    final BufferedReader br = new BufferedReader(new FileReader(oldFilename));

    String line = br.readLine();
    for (FileWriter fw : fws) {
      fw.write(line + "\n");
    }
    final String[] dimensions = line.split("x");
    final int cols = Integer.valueOf(dimensions[1]);
    line = br.readLine();

    while (line != null) {
      final String[] oldPositions = line.split("-");
      int persecutorPosition = Integer.valueOf(oldPositions[0]);
      int pursuedPosition = Integer.valueOf(oldPositions[1]);
      for (FileWriter fw : fws) {
        persecutorPosition = rotate(persecutorPosition, cols);
        pursuedPosition = rotate(pursuedPosition, cols);
        fw.write(String.valueOf(persecutorPosition) + '-' +
                String.valueOf(pursuedPosition) + "\n");
      }

      for (int i = 0; i < AVOIDABLE_LINES; i++) {
        line = br.readLine();
        for (FileWriter fw : fws) {
          fw.write(line + "\n");
        }
      }
      line = br.readLine();
    }

    end(fws, br);

  }

  private static int rotate(final int oldNumber, final int cols) {
    final int[] newPosition = new int[]{oldNumber % cols, cols - 1 - (oldNumber / cols)};
    return newPosition[0] * cols + newPosition[1];
  }

  private static void end(final List<FileWriter> fws, final BufferedReader br) throws IOException {
    for (FileWriter fw : fws) {
      fw.close();
    }
    br.close();
  }

}
