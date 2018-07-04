import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class Main {
	public static void main(String[] argv) throws Exception {

		// Process process = new ProcessBuilder(/* codesys exe */).start();
		// Process process2 =
		// Runtime.getRuntime().exec("H:\\autonomesAuto\\autonomes_Auto\\misc\\udpServer.py");
		String[] command = { System.getenv("WINDIR")
				+ "\\System32\\cmd.exe \"/K\" C:\\Users\\jalak\\Anaconda3\\Scripts\\activate.bat C:\\Users\\jalak\\Anaconda3" };
		Process p = Runtime.getRuntime().exec(command);
		new Thread(new SyncPipe(p.getErrorStream(), System.err)).start();
		new Thread(new SyncPipe(p.getInputStream(), System.out)).start();
		PrintWriter stdin = new PrintWriter(p.getOutputStream());
		stdin.println("C:");
		stdin.println("cd Users\\jalak\\Desktop\\car\\record");
		stdin.println("C:\\Users\\jalak\\Anaconda3\\Scripts\\activate.bat");
		stdin.println("activate tensorflow");
		stdin.println("python Server.py");
		// Hier Befehle einfügen
		stdin.close();
		int returnCode = p.waitFor();
		System.out.println("Return code = " + returnCode);

	}
}
