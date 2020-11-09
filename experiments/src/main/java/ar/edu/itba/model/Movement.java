package ar.edu.itba.model;

public enum Movement {

  UP(-1, 0),
  DOWN(1, 0),
  LEFT(0, -1),
  RIGHT(0, 1),;

  private final int[] movement;

  Movement(final int rowOffset, final int colOffset) {
    this.movement = new int[]{rowOffset, colOffset};
  }

  public int[] getMovement() {
    return movement;
  }
}
