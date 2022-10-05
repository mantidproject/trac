#include "Poco/Process.h"
#include "Poco/PipeStream.h"
#include "Poco/StreamCopier.h"
#include <sstream>
#include <iostream>

using Poco::Process;
using Poco::ProcessHandle;

int main(int argc, char** argv)
{
  std::string cmd("/home/dmn58364/Builds/paraview-3.10/release/bin/paraview");
  std::vector<std::string> args;
  args.push_back("-V");
  Poco::Pipe outPipe, errPipe;
  ProcessHandle ph = Process::launch(cmd, args, 0, &outPipe, &errPipe);
  // Read from the pipes
  Poco::PipeInputStream stdout(outPipe), stderr(errPipe);
  std::ostringstream outStream, errStream;
  Poco::StreamCopier::copyStream(stdout, outStream);
  Poco::StreamCopier::copyStream(stderr, errStream);
  std::cout << "stdout =\"" << outStream.str() << "\"\n";
  std::cout << "stderr =\"" << errStream.str() << "\"\n";
  return 0;
}

