package ar.edu.itba.model;

import java.time.Duration;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.geometry.Pos;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.Text;

public class CounterPane extends VBox {

  private static final String TITLE_MESSAGE = "Starting in...";
  private static final Duration DURATION = Duration.ofSeconds(5);

  private final Text title;
  private final Text counter;
  private final Timeline timeline;
  private Duration timeRemaining;

  public CounterPane() {
    this.title = new Text(TITLE_MESSAGE);
    this.title.setFont(Font.font(36));
    this.title.setFill(Color.WHITE);
    this.counter = new Text(String.valueOf(DURATION.getSeconds()));
    this.counter.setFont(Font.font(50));
    this.counter.setFill(Color.WHITE);
    this.timeRemaining = DURATION;
    this.timeline = new Timeline();
    this.timeline.setCycleCount((int) DURATION.getSeconds());
    this.timeline.getKeyFrames().add(new KeyFrame(javafx.util.Duration.seconds(1), e -> {
      timeRemaining = timeRemaining.minusSeconds(1);
      counter.setText(String.valueOf(timeRemaining.getSeconds()));
    }));
    this.timeline.setOnFinished(e -> {
      timeRemaining = DURATION;
      counter.setText(String.valueOf(DURATION.getSeconds()));
    });
    this.getChildren().addAll(title, new Text(""), counter);
    this.setAlignment(Pos.CENTER);
  }

  public void setOnTimerFinished(final Runnable runnable) {
    this.timeline.setOnFinished(e -> {
      timeRemaining = DURATION;
      counter.setText(String.valueOf(DURATION.getSeconds()));
      runnable.run();
    });
  }

  public void startTimer() {
    timeRemaining = DURATION;
    counter.setText(String.valueOf(DURATION.getSeconds()));
    timeline.playFromStart();
  }
}
