from setuptools import setup

setup(
    name="aisle_driver",
    version="0.1.0",
    packages=["aisle_driver"],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/aisle_driver"]),
        ("share/aisle_driver", ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    entry_points={"console_scripts": ["drive_aisle = aisle_driver.drive_aisle:main"]},
)
