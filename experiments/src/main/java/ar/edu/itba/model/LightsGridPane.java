package ar.edu.itba.model;

import java.util.Arrays;
import javafx.geometry.Pos;
import javafx.scene.layout.GridPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Shape;

public class LightsGridPane extends GridPane {

  private static final Color PERSECUTOR_COLOR = Color.BLUE;
  private static final Color PURSUED_COLOR = Color.MEDIUMSEAGREEN;
  private static final Color EMPTY_COLOR = Color.DARKGRAY;
  private static final Color WIN_COLOR = Color.RED;

  private static final int GAP_SIZE = 12;
  private static final int SHAPE_SIZE = 40;

  private final int rows;
  private final int cols;
  private final Shape[][] shapes;

  private final int[] persecutorPosition;
  private final int[] pursuedPosition;

  public LightsGridPane(final int rows, final int cols, final int[] persecutorPosition,
      final int[] pursuedPosition) {
    this.rows = rows;
    this.cols = cols;
    this.shapes = new Shape[rows][cols];
    this.pursuedPosition = Arrays.copyOf(pursuedPosition, pursuedPosition.length);
    this.persecutorPosition = Arrays.copyOf(persecutorPosition, persecutorPosition.length);

    for (int row = 0; row < rows; row++) {
      for (int col = 0; col < cols; col++) {
        final Shape rec = new Circle(SHAPE_SIZE, EMPTY_COLOR);
        this.shapes[row][col] = rec;
        this.add(rec, col, row);
      }
    }

    this.shapes[this.persecutorPosition[0]][this.persecutorPosition[1]].setFill(PERSECUTOR_COLOR);
    this.shapes[pursuedPosition[0]][pursuedPosition[1]].setFill(PURSUED_COLOR);

    this.setHgap(GAP_SIZE);
    this.setVgap(GAP_SIZE);
    this.setLayoutX(GAP_SIZE);
    this.setLayoutY(GAP_SIZE);
    this.setAlignment(Pos.CENTER);
  }

  public void movePersecutorWithOffset(final int[] offset){
    moveLightWithOffset(persecutorPosition, offset, PERSECUTOR_COLOR);
  }

  public void movePursuedWithOffset(final int[] offset){
    moveLightWithOffset(pursuedPosition, offset, PURSUED_COLOR);
  }

  private void moveLightWithOffset(final int[] position, final int[] offset, final Color color) {
    shapes[position[0]][position[1]].setFill(EMPTY_COLOR);
    position[0] += offset[0];
    position[1] += offset[1];
    if (Arrays.equals(persecutorPosition, pursuedPosition)) {
      shapes[position[0]][position[1]].setFill(WIN_COLOR);
    } else {
      shapes[position[0]][position[1]].setFill(color);
    }
  }

  public boolean isValidOffset(int[] movement) {
    int newRow = persecutorPosition[0] + movement[0];
    int newCol = persecutorPosition[1] + movement[1];
    return newRow >= 0 && newRow < rows && newCol >= 0 && newCol < cols;
  }
}
