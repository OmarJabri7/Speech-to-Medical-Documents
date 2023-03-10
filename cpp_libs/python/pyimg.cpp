#include <pybind11/pybind11.h>
#include "img_libs.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pyimg, m) {
    py::class_<ImgUtils>(m, "ImgUtils")
        .def(py::init<>())
        .def("analyze_doc", &ImgUtils::analyze_doc);
}
