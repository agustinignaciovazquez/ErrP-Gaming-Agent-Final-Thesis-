package ar.edu.itba.experiments;

import ar.edu.itba.io.GridFileReader;
import ar.edu.itba.io.senders.PersecutorSender;
import ar.edu.itba.io.senders.StimulusSender;
import ar.edu.itba.model.*;
import ar.edu.itba.model.behaviours.LeftRightBehaviour;
import ar.edu.itba.model.behaviours.MovementBehaviour;
import ar.edu.itba.model.behaviours.UpDownBehaviour;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Rectangle2D;
import javafx.scene.Scene;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.CornerRadii;
import javafx.scene.paint.Color;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.awt.*;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Collectors;

import static java.lang.Math.abs;

public class GridLightsReplicate extends Application {

  private static final Random RANDOM = ThreadLocalRandom.current();
  private static final List<MovementBehaviour> MOVEMENT_BEHAVIOURS = Arrays.asList(new LeftRightBehaviour(), new UpDownBehaviour());
  private static final List<MovementBehaviour> NEVER_MOVE = Collections.singletonList((p, r, c) -> new int[]{0, 0});
  private static final List<MovementBehaviour> MOVEMENTS = NEVER_MOVE;
  private static int EXPERIMENTS = 5;
  private static final int ROWS = 5;
  private static final int COLS = 5;
  private static final boolean SEND_STIMULUS = false;
  private static final boolean SEND_POSITION = true;
  private static final Duration STEP_DURATION = Duration.seconds(2);

  private static final String HOST = "10.17.2.165";
  private static final int PORT = 15361;

  private static final String HOST_POSITION = "127.0.0.1";
  private static final int PORT_POSITION = 669;

  private static int experimentNo = 0;
  private static int[] persecutorPosition;
  private int[] pursuedPosition;

  private static final String START = "start";
  private static final String FINISH = "finish";
  private static final String CLOSER = "closer";
  private static final String SAME_DISTANCE = "same distance";
  private static final String FURTHER = "further";
  private static final String[] LABELS = new String[]{START, FINISH, CLOSER, SAME_DISTANCE, FURTHER};
  private static final EventsCounter EVENTS_COUNTER = new EventsCounter(LABELS);

  private static final String FILENAME = "kk";

  private static LightsGridPane CURRENT_GRID;
  private BorderPane pane;
  private CounterPane counterPane;

  private static GridFileReader gridFileReader;
  private static Point dimension;

  private static Function<String, Point> GET_MOVEMENT;
  private static Function<String, int[]> RANDOM_MOVEMENT = (state) -> {
    final List<int[]> validMovements = Arrays.stream(Movement.values())
            .map(Movement::getMovement)
            .filter(CURRENT_GRID::isValidOffset)
            .collect(Collectors.toList());
    return validMovements.get(RANDOM.nextInt(validMovements.size()));
  };

  public static void main(String[] args) throws IOException {
    if (args.length == 0) {
      //GET_MOVEMENT = RANDOM_MOVEMENT;
      throw new IllegalArgumentException();
    } else {
      System.out.println("Leyendo archivo");
      for (int i = 0; i < args.length; i ++) {
        if (i == 0){
          gridFileReader = new GridFileReader(args[i]);
        }else {
          gridFileReader.addNewGame(args[i]);
        }
      }
      dimension = gridFileReader.getDimesions();
      EXPERIMENTS = gridFileReader.getGamesLoaded();

      GET_MOVEMENT = (state) -> {
        Point action = gridFileReader.getNextPosition();
        int x = (action.x % COLS) - persecutorPosition[1];
        int y = ((action.x - x) / COLS) - persecutorPosition[0];
        return new Point(x,y);
    };
    }

    launch(args);
  }

  @Override
  public void start(Stage primaryStage) {
    final StartScreen startScreen = new StartScreen();
    startScreen.setOnStart(() -> {
      pane.setCenter(counterPane);
      counterPane.startTimer();
    });

    counterPane = new CounterPane();
    counterPane.setOnTimerFinished(() -> {
      try {
        startExperiment();
      } catch (IOException e) {
        e.printStackTrace();
      }
    });

    pane = new BorderPane(startScreen);
    pane.setBackground(
            new Background(new BackgroundFill(Color.BLACK, CornerRadii.EMPTY, Insets.EMPTY)));

    primaryStage.setTitle("Square Lights");
    primaryStage.setScene(new Scene(pane));
    primaryStage.setResizable(false);
    primaryStage.setMaximized(true);
    setMaxSize(primaryStage);
    primaryStage.setFullScreen(true);
    primaryStage.show();
  }

  private static void setMaxSize(final Stage primaryStage) {
    final Screen screen = Screen.getPrimary();
    final Rectangle2D bounds = screen.getVisualBounds();

    primaryStage.setX(bounds.getMinX());
    primaryStage.setY(bounds.getMinY());
    primaryStage.setWidth(bounds.getWidth());
    primaryStage.setHeight(bounds.getHeight());
  }

  private void startExperiment() throws IOException {
    FileWriter fileWriter = new FileWriter(FILENAME + '_' + String.valueOf(experimentNo));
    fileWriter.write(String.valueOf(ROWS) + 'x' + String.valueOf(COLS));
    fileWriter.write('\n');
    EVENTS_COUNTER.count(START);

    MovementBehaviour behaviour = initExperiment();
    fileWriter.write(stateToString() + "\n\n");

    final StimulusSender sender = new StimulusSender();
    final PersecutorSender senderPosition = new PersecutorSender();

    if (SEND_STIMULUS) {
      try {
        sender.open(HOST, PORT);
        sender.send(3L, 0L);
      } catch (final IOException e) {
        e.printStackTrace();
        return;
      }
    }

    if (SEND_POSITION) {
      try {
        senderPosition.open(HOST_POSITION, PORT_POSITION);
        //senderPosition.send(persecutorStateToInt(), pursuedStateToInt(), gridFileReader.getDimesions(), gridFileReader.getGamesLoaded());
      } catch (final IOException e) {
        e.printStackTrace();
        return;
      }
    }

    final Timeline timeline = new Timeline();
    final KeyFrame keyFrame = new KeyFrame(STEP_DURATION, e -> {
      experimentIteration(fileWriter, timeline, sender, senderPosition, behaviour);
    });
    timeline.getKeyFrames().add(keyFrame);
    timeline.setCycleCount(Timeline.INDEFINITE);
    timeline.play();
  }

  private MovementBehaviour initExperiment() {
    persecutorPosition = newStartingPosition();
    pursuedPosition = newPursuedPosition();
    CURRENT_GRID = new LightsGridPane(ROWS, COLS, persecutorPosition, pursuedPosition);
    pane.setCenter(CURRENT_GRID);
    return MOVEMENTS.get(RANDOM.nextInt(MOVEMENTS.size()));
  }

  private void experimentIteration(FileWriter fileWriter, Timeline timeline, StimulusSender sender,
                                   PersecutorSender persecutorSender, MovementBehaviour behaviour) {
    final int prevDistance = distanceToPursued(pursuedPosition);
    final Point offsetMovement = GET_MOVEMENT.apply(stateToString());
    final int[] movement = new int[]{offsetMovement.y, offsetMovement.x};
    moveLightWithOffset(persecutorPosition, movement, CURRENT_GRID::movePersecutorWithOffset);

    if (!Arrays.equals(persecutorPosition, pursuedPosition)) {
      moveLightWithOffset(pursuedPosition, behaviour.getOffset(pursuedPosition, ROWS, COLS),
              CURRENT_GRID::movePursuedWithOffset);
    }

    if (SEND_POSITION) {
      try {
        persecutorSender.send(persecutorStateToInt(),pursuedStateToInt(), gridFileReader.getDimesions(), gridFileReader.getGamesLoaded());
      } catch (Exception exception) {
        exception.printStackTrace();
      }
    }

    try {
      fileWriter.write(stateToString() + "\n\n");
    } catch (IOException e1) {
      e1.printStackTrace();
    }

    if (distanceToPursued(pursuedPosition) == 0) {
      EVENTS_COUNTER.count(FINISH, CLOSER);
      timeline.stop();
      try {
        fileWriter.close();
      } catch (IOException e1) {
        e1.printStackTrace();
      }
      if (SEND_STIMULUS) {
        try {
          sender.send(4L, 0L);
          sender.close();
        } catch (Exception e1) {
          e1.printStackTrace();
        }
      }
      if (SEND_POSITION) {
        try {
          //sender.send(4L, 0L);
          persecutorSender.close();
        } catch (Exception e1) {
          e1.printStackTrace();
        }
      }
      if (experimentNo < EXPERIMENTS) {
        experimentNo++;
        try {
          startExperiment();
        } catch (IOException e) {
          e.printStackTrace();
        }
      } else {
        System.out.println(EVENTS_COUNTER);
      }
    } else {
      final int currentDistance = distanceToPursued(pursuedPosition);
      final long distanceDifference = prevDistance - currentDistance;
      EVENTS_COUNTER.count(getLabelByDistanceDifference(distanceDifference));
      if (SEND_STIMULUS) {
        try {
          sender.send(distanceDifference >= 0 ? 1 : 2, 0L);
        } catch (Exception exception) {
          exception.printStackTrace();
        }
      }
    }

  }

  private void moveLightWithOffset(int[] position, final int[] offset, final Consumer<int[]> consumer) {
    position[0] += offset[0];
    position[1] += offset[1];
    consumer.accept(offset);
  }

  private int[] newStartingPosition() {
//    return new int[]{RANDOM.nextInt(ROWS), RANDOM.nextInt(COLS)};
    return new int[]{0, 0};
  }

  private int[] newPursuedPosition() {
//    int[] pursuedPosition;
//
//    do {
//      pursuedPosition = new int[]{RANDOM.nextInt(ROWS), RANDOM.nextInt(COLS)};
//    } while (distanceToPursued(pursuedPosition) <= 1);
//
//    return pursuedPosition;
    return new int[]{ROWS - 1, COLS - 1};
  }

  private int distanceToPursued(final int[] goalPosition) {
    return abs(persecutorPosition[0] - goalPosition[0]) + abs(persecutorPosition[1] - goalPosition[1]);
  }

  private String getLabelByDistanceDifference(final long distanceDifference) {
    if (distanceDifference == 0) {
      return SAME_DISTANCE;
    }
    return distanceDifference > 0 ? CLOSER : FURTHER;
  }

  private String stateToString() {
    final int persecutor = persecutorStateToInt();
    final int pursued = pursuedStateToInt();
    return persecutor + "-" + pursued;
  }
  private int persecutorStateToInt() {
    final int persecutor = persecutorPosition[0] * COLS + persecutorPosition[1];
    return persecutor;
  }
  private int pursuedStateToInt() {
    final int pursued = pursuedPosition[0] * COLS + pursuedPosition[1];
    return pursued;
  }
}
