/* CourseLookup.cpp
 Kristian Sotiri
 Advising Assistance Program
 12/12/24
*/

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <sstream>
#include <algorithm>
using namespace std;

// Struct to represent a Course
struct Course {
    string courseNumber;
    string courseTitle;
    vector<string> prerequisites;

    // Constructor to initialize course details
    Course(string courseNumber, string courseTitle, vector<string> prerequisites)
        : courseNumber(courseNumber), courseTitle(courseTitle), prerequisites(prerequisites) {
    }
};

// Function to trim leading spaces
string trimLeadingSpaces(const string& str) {
    size_t start = 0;
    // Skip leading whitespace characters
    while (start < str.length() && (str[start] == ' ' || str[start] == '\t')) {
        ++start;
    }
    return str.substr(start);
}

// Function to trim trailing spaces
string trimTrailingSpaces(const string& str) {
    size_t end = str.length();
    // Skip trailing whitespace characters
    while (end > 0 && (str[end - 1] == ' ' || str[end - 1] == '\t')) {
        --end;
    }
    return str.substr(0, end);
}

// Function to load course data and store it in a vector data structure
vector<Course> loadCourseData(const string& filename) {
    ifstream file(filename);
    vector<Course> courses;
    set<string> courseNumbersSet;  // Set for fast prerequisite lookup

    if (!file.is_open()) {
        cout << "Error: File not found or cannot be opened" << endl;
        return courses;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string courseNumber, courseTitle;
        vector<string> prerequisites;
        string prerequisite;

        // Read course number and title
        getline(ss, courseNumber, ',');
        getline(ss, courseTitle, ',');

        // Trim leading and trailing spaces
        courseNumber = trimLeadingSpaces(courseNumber);
        courseNumber = trimTrailingSpaces(courseNumber);
        courseTitle = trimLeadingSpaces(courseTitle);
        courseTitle = trimTrailingSpaces(courseTitle);

        // Read available prerequisites
        while (getline(ss, prerequisite, ',')) {
            prerequisite = trimLeadingSpaces(prerequisite);
            prerequisite = trimTrailingSpaces(prerequisite);  // Trim spaces
            prerequisites.push_back(prerequisite);
        }

        // Validate that course number and title exist
        if (courseNumber.empty() || courseTitle.empty()) {
            cout << "Error: Invalid line format. Each line must include course number and title." << endl;
            continue;
        }

        // Add the course to the vector
        courses.push_back(Course(courseNumber, courseTitle, prerequisites));
        // Add course number to the set for future prerequisite lookup
        courseNumbersSet.insert(courseNumber);
    }

    file.close();
    cout << "Data loaded successfully from " << filename << endl;
    return courses;
}

// Function to print all courses sorted by course number
void printCourses(vector<Course>& courses) {
    // Sort courses by course number
    sort(courses.begin(), courses.end(), [](const Course& a, const Course& b) {
        return a.courseNumber < b.courseNumber;
        });

    // Print sorted courses
    for (const Course& course : courses) {
        cout << course.courseNumber << ", " << course.courseTitle << endl;
    }
}

// Function to search for a specific course and print details
void searchCourse(const vector<Course>& courses, const string& courseNumber) {
    for (const Course& course : courses) {
        if (course.courseNumber == courseNumber) {
            cout << "Course Number: " << course.courseNumber << endl;
            cout << "Course Title: " << course.courseTitle << endl;

            if (course.prerequisites.empty()) {
                cout << "No prerequisites." << endl;
            }
            else {
                cout << "Prerequisites: " << endl;
                for (const string& prereq : course.prerequisites) {
                    cout << "- " << prereq << endl;
                }
            }
            return;
        }
    }

    cout << "Course " << courseNumber << " not found in the course list." << endl;
}

// Function to display the menu options
void displayMenu() {
    cout << endl;
    cout << "1. Load Data Structure." << endl;
    cout << "2. Print Course List." << endl;
    cout << "3. Print Course." << endl;
    cout << "9. Exit" << endl;
}

int main() {
    vector<Course> courses;
    string filename;
    int option;

    cout << "Welcome to the course planner." << endl;
    while (true) {
        displayMenu();
        cout << endl;
        cout << "What would you like to do? ";
        
        // Read the menu option and validate input
        if (!(cin >> option)) {
            // If the input is not a number, clear the input buffer and prompt the user again
            cout << "Invalid input. Please enter a valid number." << endl;
            cin.clear();  // Clears the error flag
            cin.ignore(numeric_limits<streamsize>::max(), '\n');  // Discards invalid input
            continue;
        }

        // Clear the remaining newline character after reading the option
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        switch (option) {
        case 1:
            cout << "Enter the filename: ";
            getline(cin, filename);
            courses = loadCourseData(filename);  // Load data into the vector
            break;

        case 2:
            if (courses.empty()) {
                cout << "No data loaded. Please load the data first." << endl;
            }
            else {
                cout << "Here is a sample schedule:" << endl << endl;
                printCourses(courses);  // Print all courses
            }
            break;

        case 3:
            if (courses.empty()) {
                cout << "No data loaded. Please load the data first." << endl;
            }
            else {
                cout << "What course do you want to know about? ";
                string courseNumber;
                getline(cin, courseNumber);
                searchCourse(courses, courseNumber);  // Search for specific course
            }
            break;

        case 9:
            cout << "Thank you for using the course planner!" << endl;
            return 0;

        default:
            cout << option << " is not a valid option." << endl;
            break;
        }
    }

    return 0;
}
