package ar.edu.itba.io.senders;

import java.io.Closeable;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/*
 * Primitive TCP Tagging java client for OpenViBE 1.2.x
 *
 * @author Jussi T. Lindgren / Inria
 * @date 04.Jul.2016
 * @version 0.1
 */
public class StimulusSender implements AutoCloseable, Closeable {

  private Socket clientSocket;
  private DataOutputStream outputStream;

  /**
   * Open connection to Acquisition Server TCP Tagging
   */
  public void open(final String host, final int port) throws IOException {
    clientSocket = new Socket(host, port);
    outputStream = new DataOutputStream(clientSocket.getOutputStream());
  }

  // Close connection
  @Override
  public void close() throws IOException {
    clientSocket.close();
  }

  // Send stimulation with a timestamp.
  public void send(long stimulation, Long timestamp) throws IOException {
    final ByteBuffer byteBuffer = ByteBuffer.allocate(24);
    byteBuffer.order(ByteOrder.LITTLE_ENDIAN); // Assumes AS runs on LE architecture
    byteBuffer.putLong(0);              // Not used
    byteBuffer.putLong(stimulation);    // Stimulation id
    byteBuffer.putLong(timestamp);      // Timestamp: 0 = immediate

    outputStream.write(byteBuffer.array());
  }
}
