package ar.edu.itba.model;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class EventsCounter {

  private final Map<String, Integer> map = new HashMap<>();

  public EventsCounter(String[] events) {
    Arrays.stream(events).forEach(event -> map.put(event, 0));
  }

  private int getValue(String event) {
    return Optional.ofNullable(map.get(event)).orElseThrow(() -> new IllegalStateException(event + "doesn't exist"));
  }

  public void count(String... events) {
    Arrays.stream(events).forEach(e -> map.put(e, getValue(e) + 1));
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    map.forEach((label, val) -> sb.append(label).append(": ").append(val).append("\n"));
    return sb.toString();
  }
}
