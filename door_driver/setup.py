from setuptools import setup

setup(
    name="door_driver",
    version="0.1.0",
    packages=["door_driver"],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/door_driver"]),
        ("share/door_driver", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    tests_require=["pytest"],
    zip_safe=True,
    entry_points={"console_scripts": ["drive_forward = door_driver.drive_forward:main"]},
)
