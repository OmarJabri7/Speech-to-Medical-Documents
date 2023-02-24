#include <pybind11/pybind11.h>
#include "img_libs.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pyimg, m) {
    py::class_<MyCppLibrary>(m, "MyCppLibrary")
        .def(py::init<>())
        .def("add", &MyCppLibrary::add);
}
