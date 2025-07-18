from setuptools import setup
import os
import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


# Get PyTorch library directory
torch_lib_dir = os.path.join(os.path.dirname(torch.__file__), 'lib')
rpath_flag = f"-Wl,-rpath,{torch_lib_dir}"

ROOT = os.path.dirname(os.path.abspath(__file__))
extra_compile_args = {
    # "cores": ["j8"],
    "cxx": ["-O2"],
    "nvcc": ["-O2"],
}

setup(
    name="lietorch",
    version="0.3",
    description="Lie Groups for PyTorch",
    author="Zachary Teed",
    packages=["lietorch"],
    ext_modules=[
        CUDAExtension("lietorch_backends", 
            include_dirs=[
                os.path.join(ROOT, "lietorch/include"), 
                os.path.join(ROOT, "eigen")
            ],
            sources=[
                "lietorch/src/lietorch.cpp", 
                "lietorch/src/lietorch_gpu.cu",
                "lietorch/src/lietorch_cpu.cpp"
            ],
            extra_compile_args=extra_compile_args,
            extra_link_args=[rpath_flag]),

        CUDAExtension("lietorch_extras", 
            sources=[
                "lietorch/extras/altcorr_kernel.cu",
                "lietorch/extras/corr_index_kernel.cu",
                "lietorch/extras/se3_builder.cu",
                "lietorch/extras/se3_inplace_builder.cu",
                "lietorch/extras/se3_solver.cu",
                "lietorch/extras/extras.cpp",
            ],
            extra_compile_args=extra_compile_args,
            extra_link_args=[rpath_flag]),
    ],
    cmdclass={ "build_ext": BuildExtension }
)
