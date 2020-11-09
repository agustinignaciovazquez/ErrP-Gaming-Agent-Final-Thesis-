package ar.edu.itba.model.behaviours;

import java.util.Random;

public class UpDownBehaviour implements MovementBehaviour {

  private int direction;

  public UpDownBehaviour() {
    final Random r = new Random();
    direction = r.nextBoolean() ? 1 : -1;
  }

  @Override
  public int[] getOffset(final int[] position, final int rows, final int cols) {
    if (rows == 1) {
      return new int[]{0, 0};
    }

    if (position[0] + direction < 0 || position[0] + direction > rows - 1) {
      direction *= -1;
    }

    return new int[]{direction, 0};
  }
}
