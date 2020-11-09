package ar.edu.itba.io.senders;

import java.awt.*;
import java.io.Closeable;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/*
 * Primitive TCP Tagging java client for OpenViBE 1.2.x
 *
 * @author Agustin Vazquez
 * @date 04.Jul.2016
 * @version 0.1
 */
public class PersecutorSender implements AutoCloseable, Closeable {

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
  public void send(int persecutor, int pursued, Point dim, int games_loaded) throws IOException {
    final ByteBuffer byteBuffer = ByteBuffer.allocate(20);
    byteBuffer.order(ByteOrder.BIG_ENDIAN); // Assumes AS runs on LE architecture
    byteBuffer.putInt(dim.x);              // Dimension X
    byteBuffer.putInt(dim.y);              // Dimension Y
    byteBuffer.putInt(games_loaded);             // Games loaded
    byteBuffer.putInt(persecutor);    // Persecutor position
    byteBuffer.putInt(pursued);      // Pursued position
    outputStream.write(byteBuffer.array());
    System.out.println("persecutor: "+persecutor);
  }
}
