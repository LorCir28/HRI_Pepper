/**
 *
 * This example demonstrates how to get images from the robot remotely and how
 * to display them on your screen using opencv.
 *
 * Copyright Aldebaran Robotics
 */

// Opencv includes.
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

// Aldebaran includes.
#include <alproxies/alvideodeviceproxy.h>
#include <alvision/alimage.h>
#include <alvision/alvisiondefinitions.h>
#include <alerror/alerror.h>

// Boost includes.
#include <boost/program_options.hpp>

#include <iostream>
#include <string>

using namespace AL;


/**
* \brief Shows images retrieved from the robot.
*
* \param robotIp the IP adress of the robot
*/
void showImages(const std::string& robotIp, int port)
{

  /** Create a proxy to ALVideoDevice on the robot.*/
  ALVideoDeviceProxy camProxy(robotIp, port);

  /** Subscribe a client image requiring 320*240 and BGR colorspace.*/
  const std::string clientName = camProxy.subscribe("test", kQVGA, kBGRColorSpace, 30);

  /** Create an cv::Mat header to wrap into an opencv image.*/
  cv::Mat imgHeader = cv::Mat(cv::Size(320, 240), CV_8UC3);

  /** Create a OpenCV window to display the images. */
  cv::namedWindow("images");

  /** Main loop. Exit when pressing ESC.*/
  while ((char) cv::waitKey(30) != 27)
  {
    /** Retrieve an image from the camera.
    * The image is returned in the form of a container object, with the
    * following fields:
    * 0 = width
    * 1 = height
    * 2 = number of layers
    * 3 = colors space index (see alvisiondefinitions.h)
    * 4 = time stamp (seconds)
    * 5 = time stamp (micro seconds)
    * 6 = image buffer (size of width * height * number of layers)
    */
    ALValue img = camProxy.getImageRemote(clientName);

    /** Access the image buffer (6th field) and assign it to the opencv image
    * container. */
    imgHeader.data = (uchar*) img[6].GetBinary();

    /** Tells to ALVideoDevice that it can give back the image buffer to the
    * driver. Optional after a getImageRemote but MANDATORY after a getImageLocal.*/
    camProxy.releaseImage(clientName);

    /** Display the iplImage on screen.*/
    cv::imshow("images", imgHeader);
  }

  /** Cleanup.*/
  camProxy.unsubscribe(clientName);
}



int main(int argc, char** argv)
{
  namespace po = boost::program_options;

  po::options_description description("Options");
  description.add_options()
    ("help", "Displays this help message")
    ("pip", po::value<std::string>()->default_value(std::getenv("PEPPER_IP")), "Robot IP address.  On robot or Local Naoqi: use '127.0.0.1'.")
    ("pport", po::value<int>()->default_value(9559), "Naoqi port number.")
    ;

  po::variables_map vm;
  po::store(po::parse_command_line(argc, argv, description), vm);
  po::notify(vm);
  
  // --help option
  if (vm.count("help")){ 
    std::cout << description << std::endl; 
    return 0; 
  } 

  const std::string pip = vm["pip"].as<std::string>();
  int pport = vm["pport"].as<int>();
  
  showImages(pip, pport);
  
}

