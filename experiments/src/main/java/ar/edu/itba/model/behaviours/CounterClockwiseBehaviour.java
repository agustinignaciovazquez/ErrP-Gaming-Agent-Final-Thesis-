package ar.edu.itba.model.behaviours;

import com.sun.javafx.scene.traversal.Direction;

public class CounterClockwiseBehaviour extends CircularBehaviour {

  @Override
  public int[] getOffset(final int[] position, final int rows, final int cols) {
    if (!isInBorder(position, rows, cols)) {
      this.direction = whereToMove(position, rows, cols);
    } else {
      if (position[0] == 0 && position[1] > 0) {
        this.direction = Direction.LEFT;
      } else if (position[0] < rows - 1 && position[1] == 0) {
        this.direction = Direction.DOWN;
      } else if (position[0] == rows - 1 && position[1] < cols - 1) {
        this.direction = Direction.RIGHT;
      } else {
        this.direction = Direction.UP;
      }
    }
    return MAP.get(this.direction);
  }

}
