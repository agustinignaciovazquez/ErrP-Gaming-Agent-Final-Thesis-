package ar.edu.itba.model.behaviours;

public interface MovementBehaviour {

  int[] getOffset(final int[] position, final int rows, final int cols);

}
