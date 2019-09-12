# Analyzing NPM packages
This is a project that aims to understand the existing npm packages and libraries using Qualitative and Statistical Analysis using the r2c analyzer.

The following Analysis has been done:
### Trivial packages:
Out of the 1000 npm packages, number of trivial packages were identified. Trivial package is any package which has less than 35 lines of code and cyclomatic complexity less than 10.

### Time lag of dependencies:
The dependencies of each package was identified and the Time Lag between the latest version of the dependency and the version used in the project was computed for all packages.

### Dependency Tree:
The dependency tree for each package was computed and cyclic dependencies were identified.

### Statistical Analysis
Statistical analysis such as goodness of fit, t-test and correlation analysis were done on all 1000 packages.

