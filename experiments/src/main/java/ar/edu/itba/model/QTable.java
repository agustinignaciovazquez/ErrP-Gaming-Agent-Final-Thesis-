package ar.edu.itba.model;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.function.Predicate;

public class QTable {

  private static final Random RANDOM = new Random();

  private final Map<String, Integer> states = new TreeMap<>();
  private final Map<Integer, String> actions = new TreeMap<>();
  private final double[][] table;

  public QTable(final String filename) throws IOException {
    final BufferedReader br = new BufferedReader(new FileReader(filename));

    String line = br.readLine();
    final String[] dimension = line.split("x");
    table = new double[Integer.valueOf(dimension[0])][Integer.valueOf(dimension[1])];

    for (int i = 0; i < table.length; i++) {
      line = br.readLine();
      states.put(line, i);
    }

    for (int i = 0; i < table[0].length; i++) {
      line = br.readLine();
      actions.put(i, line);
    }

    for (int row = 0; row < table.length; row++) {
      for (int col = 0; col < table[0].length; col++) {
        table[row][col] = Double.valueOf(br.readLine());
      }
    }

    br.close();
  }

  public String getRecommendedAction(final String state, Predicate<String> isValidAction) {
    final double[] row = table[states.get(state)];
    double max = Double.NEGATIVE_INFINITY;
    List<String> bestActions = new ArrayList<>();
    List<String> validActions = new ArrayList<>();
    for (Map.Entry<Integer, String> entry : actions.entrySet()) {
      if (isValidAction.test(entry.getValue())) {
        validActions.add(entry.getValue());
        if (row[entry.getKey()] >= max) {
          if (row[entry.getKey()] > max) {
            max = row[entry.getKey()];
            bestActions.clear();
          }
          bestActions.add(entry.getValue());
        }
      }
    }

    if (RANDOM.nextDouble() < 0.5) {
      return validActions.get(RANDOM.nextInt(validActions.size()));
    }
    return bestActions.get(RANDOM.nextInt(bestActions.size()));
  }

}
