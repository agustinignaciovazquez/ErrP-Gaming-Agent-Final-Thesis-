package ar.edu.itba.model.behaviours;

import com.sun.javafx.scene.traversal.Direction;

import java.util.HashMap;
import java.util.Map;

public abstract class CircularBehaviour implements MovementBehaviour {

  protected static final Map<Direction, int[]> MAP = new HashMap<>();
  protected Direction direction;

  static {
    MAP.put(Direction.UP, new int[]{-1, 0});
    MAP.put(Direction.DOWN, new int[]{1, 0});
    MAP.put(Direction.LEFT, new int[]{0, -1});
    MAP.put(Direction.RIGHT, new int[]{0, 1});
  }

  protected boolean isInBorder(final int[] position, final int rows, final int cols) {
    return position[0] == 0 || position[0] == rows - 1 || position[1] == 0 || position[1] == cols - 1;
  }

  protected Direction whereToMove(final int[] position, final int rows, final int cols) {
    Direction[] directions = new Direction[]{Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT};
    int[] distances = new int[]{position[0], Math.abs(position[1] - (cols - 1)), Math.abs(position[0] - (rows - 1)), position[1]};

    int minDistance = distances[0];
    Direction direction = directions[0];

    for (int i = 1; i < 3; i++) {
      if (distances[i] < minDistance) {
        minDistance = distances[i];
        direction = directions[i];
      }
    }

    return direction;
  }
}
