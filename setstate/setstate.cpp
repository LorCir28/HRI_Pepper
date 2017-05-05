/**
 * Copyright (c) 2011 Aldebaran Robotics. All Rights Reserved
 * \file sayhelloworld.cpp
 * \brief Make NAO say a short phrase.
 *
 * A simple example showing how to make NAO say a short phrase using the
 * specialized proxy ALTextToSpeechProxy.
 */


#include <iostream>
#include <alerror/alerror.h>
#include <alproxies/altexttospeechproxy.h>
#include <alproxies/alautonomouslifeproxy.h>
#include <alproxies/alrobotpostureproxy.h>

#include <alcommon/alproxy.h>
#include <alcommon/albroker.h>

int main(int argc, char* argv[])
{
  if(argc != 3)
  {
    std::cerr << "Wrong number of arguments!" << std::endl;
    std::cerr << "Usage: setstate PEPPER_IP state" << std::endl;
    exit(2);
  }

  int pport = 9559;
  std::string pip = argv[1];
  std::string state = argv[2];
  
  // A broker needs a name, an IP and a port to listen:
  const std::string brokerName = "mybroker";
  // Create your own broker
  boost::shared_ptr<AL::ALBroker> broker =
    AL::ALBroker::createBroker(brokerName, "0.0.0.0", 54000, pip, pport);

  // Create a proxy to ALTextToSpeechProxy
  AL::ALProxy proxyTTS(broker, "ALTextToSpeech");

  AL::ALAutonomousLifeProxy proxyAL(broker);
  std::string current_state = proxyAL.getState();
  std::cerr << "Robot state: " << current_state << std::endl;
  
  /** The desired phrase to be said. */
  std::string phraseToSay = "Hello! My current state is " + current_state;
  // Call say method
  proxyTTS.callVoid("say", phraseToSay);

  if (current_state != state){
    phraseToSay = "Changing my state to " + state;
    proxyTTS.callVoid("say", phraseToSay);

    proxyAL.setState(state);

    current_state = proxyAL.getState();
    std::cerr << "Robot state: " << current_state << std::endl;
  } else {
    phraseToSay = "Nothing to change here.";
    proxyTTS.callVoid("say", phraseToSay);
  }
  /*
  std::vector<AutonomousAbilityStatus> aastatus = proxyAL.getAutonomousAbilitiesStatus();

  for (size_t i=0; i<aastatus.size(); i++){
    aastatusi = aastatus[i];
    std::cerr << "Autonomous Ability: " << aastatusi.name << std::endl;
    std::cerr << "Enabled: " << aastatusi.enabled << std::endl;
    std::cerr << "Running: " << aastatusi.running << std::endl;
  }*/

  phraseToSay = "I'm going to stand up";
  proxyTTS.callVoid("say", phraseToSay);
  
  AL::ALRobotPostureProxy proxyRP(broker);
  proxyRP.goToPosture("Stand",1.0);

  std::vector<std::string> familypostures = proxyRP.getPostureFamilyList();
  for (size_t i=0; i<familypostures.size(); i++){
    std::string fposture = familypostures[i];
    std::cerr << "Posture Family: " << fposture << std::endl;
  }

  std::vector<std::string> postures = proxyRP.getPostureList();
  for (size_t i=0; i<postures.size(); i++){
    std::string posture = postures[i];
    std::cerr << "Posture: " << posture << std::endl;
  }
  
  exit(0);
}
