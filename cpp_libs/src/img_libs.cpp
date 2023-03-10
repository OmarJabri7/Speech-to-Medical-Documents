#include "img_libs.hpp" 
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <math.h>

ImgUtils::ImgUtils() {};

void ImgUtils::analyze_doc(std::vector<std::string> folders, std::string form) {
    std::ifstream file(folders[0] + "/wordlist.txt");
    if(!file.is_open()){
        std::cout << "Cannot open file";
        exit(1);
    }
    std::vector<std::string> med_words;
    std::string line;
    while (std::getline(file, line))
        med_words.push_back(line);  
    file.close();
    cv::Mat img = cv::imread(folders[0] + "/{form}.jpeg");
}