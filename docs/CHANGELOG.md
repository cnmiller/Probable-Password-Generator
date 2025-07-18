# Changelog

All notable changes to the Password Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-01-16

### Added
- **Optional City Parameter**: City is now optional (`--city`) instead of required, allowing keywords-only generation
- **Compound Word Intelligence**: Proper handling of multi-word inputs like "New York" → "NewYork", "newyork", "NewYork2025!"
- **Advanced Prioritization**: Clean patterns like "Chase2025!!" now rank higher than artificial patterns like "Chase$251!!!"
- **Compound Title Case Scoring**: "NewYork2025!" gets priority bonus over "newyork2025!" for compound words

### Enhanced
- **Prioritization Algorithm**: Complete overhaul based on real penetration testing observations
- **Clean Pattern Detection**: Smart identification of natural user-created password patterns
- **Realistic Padding**: Simplified padding strategies focusing on patterns users actually employ
- **Command Line Interface**: More flexible usage with optional city parameter

### Fixed
- **Critical Scoring Bug**: Fixed backwards prioritization where artificial patterns ranked higher than natural ones
- **Compound Word Generation**: Multi-word inputs now properly generate all case variations
- **Length Padding**: Removed unrealistic padding patterns that don't reflect real user behavior

## [2.1.0] - 2025-01-16

### Added
- **Intelligent Length Padding**: When minimum length is specified, automatically generates realistic padding patterns (e.g., "Summer2025!!" for 12-char minimum)
- **Advanced Padding Strategies**: Duplicate symbols, sequential numbers, and mixed symbol/number patterns based on real user behavior
- **Enhanced Length Scoring**: Bonus points for passwords that exactly meet common minimum lengths (8, 10, 12, 14, 16)
- **Padding Pattern Detection**: Smart scoring system recognizes and prioritizes length-driven password modifications

### Enhanced
- **Minimum Length Intelligence**: `--min-length` parameter now triggers intelligent padding instead of just filtering
- **Real-world Accuracy**: Patterns based on penetration testing observations and user behavior studies
- **Corporate Policy Awareness**: Better handling of length requirements common in enterprise environments

## [2.0.0] - 2025-01-16

### Added
- **Generate All Combinations by Default**: Tool now generates all possible password combinations when no count is specified
- **File Output Option**: New `--output` argument to save passwords directly to files
- **Enhanced Project Structure**: Complete git project with README, LICENSE, examples, and documentation
- **Professional Documentation**: Comprehensive README with usage examples, security guidelines, and technical details

### Changed
- **Default Behavior**: Changed from generating 100 passwords to generating all combinations by default
- **Command Line Interface**: Made `--count` optional instead of required
- **Help Examples**: Updated examples to showcase new file output and all-combinations features

### Technical Improvements
- Added informative status messages showing number of passwords generated
- Enhanced error handling for file operations
- Maintained full backward compatibility with existing usage patterns

## [1.5.0] - 2025-01-15

### Added
- **Dynamic Date Intelligence**: Real-time year calculation using `datetime.now()`
- **Password Expiration Awareness**: `--expiration` parameter to filter expired month-based passwords
- **Advanced Scoring System**: Likelihood-based ranking with 200+ scoring factors
- **Enhanced Symbol Control**: `--symbols` parameter to limit to most common symbols

### Enhanced
- **Team Coverage**: Expanded to 80+ cities with comprehensive sports team data
- **College Integration**: Added FBS mascots and regional university coverage
- **Leetspeak Levels**: Three sophistication levels from basic to advanced transformations
- **Corporate Policy Compliance**: Bonus scoring for common password requirements

### Fixed
- **Priority Balancing**: Custom words no longer over-prioritized when heavily modified with leetspeak
- **Team Ranking**: Sports teams now properly ranked above heavily modified patterns
- **Length Optimization**: 8-10 character passwords prioritized for corporate policies

## [1.4.0] - 2025-01-14

### Added
- **Custom Word Integration**: Support for comma-separated lists and file input
- **Minimum Length Filtering**: `--min-length` parameter for policy compliance
- **Debug Mode**: `--debug` flag to show password scores and word types
- **File Format Support**: Custom word files with comment support

### Improved
- **Independent Word Processing**: Each word type gets separate transformation pipeline
- **Enhanced Patterns**: Multiple case patterns, seasonal combinations, symbol/number suffixes
- **Error Handling**: Comprehensive input validation and graceful error messages

## [1.3.0] - 2025-01-13

### Added
- **Multi-level Leetspeak**: Three sophistication levels with different character substitutions
- **Geographic Expansion**: Added teams across all US regions and college towns
- **Seasonal Intelligence**: Dynamic seasonal pattern generation with year combinations

### Enhanced
- **Data Quality**: Removed spaces from team names, added minor league teams
- **Pattern Variety**: Enhanced variation generation with multiple transformation levels
- **Performance**: Optimized memory usage with set operations

## [1.2.0] - 2025-01-12

### Added
- **Comprehensive Type Hints**: Full type annotation throughout codebase
- **Robust Error Handling**: Graceful failure modes with appropriate exit codes
- **Input Validation**: Parameter validation for all command line arguments

### Enhanced
- **Code Quality**: Improved maintainability and readability
- **Documentation**: Inline documentation and function descriptions
- **Security**: Input sanitization and bounds checking

## [1.1.0] - 2025-01-11

### Added
- **Sports Team Expansion**: Coverage of NFL, NBA, MLB, NHL, MLS, WNBA teams
- **College Mascots**: FBS schools and regional universities
- **Geographic Intelligence**: City-based team and school associations

### Enhanced
- **Data Coverage**: Expanded from ~30 to 80+ cities
- **Pattern Generation**: Basic transformations and combinations
- **Word Lists**: Improved sports and education coverage

## [1.0.0] - 2025-01-10

### Initial Release
- **Basic Password Generation**: City-based password candidate generation
- **Common Patterns**: Integration of common passwords and keyboard walks
- **Simple Transformations**: Basic case variations and number/symbol suffixes
- **Command Line Interface**: Simple argument parsing and output
- **Core Algorithm**: Foundation scoring and variation generation

### Features
- Geographic city input
- Sports teams and basic patterns
- Command line interface
- Single-file portability
- No external dependencies

---

## Legend
- **Added**: New features
- **Changed**: Changes in existing functionality  
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security-related changes 