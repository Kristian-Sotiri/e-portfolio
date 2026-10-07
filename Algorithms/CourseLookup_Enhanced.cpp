/*
CourseLookup_Enhanced.cpp
 Kristian Sotiri
 Advising Assistance Program
 Enhanced for ePortfolio
*/

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <limits>

using namespace std;

// Struct to represent a Course
struct Course {
    string courseNumber;
    string courseTitle;
    vector<string> prerequisites;

    Course(string courseNumber, string courseTitle, vector<string> prerequisites)
        : courseNumber(courseNumber), courseTitle(courseTitle), prerequisites(prerequisites) {}
};

// Node structure for the AVL Tree
struct Node {
    Course course;
    Node* left;
    Node* right;
    int height;

    Node(Course c) : course(c), left(nullptr), right(nullptr), height(1) {}
};

// AVL Tree Class for optimized searching and sorting
class AVLTree {
private:
    Node* root;

    // Helper function to get the height of a node
    int height(Node* node) {
        if (node == nullptr) return 0;
        return node->height;
    }

    // Helper function to get the balance factor
    int getBalance(Node* node) {
        if (node == nullptr) return 0;
        return height(node->left) - height(node->right);
    }

    // Perform a right rotation to balance the tree
    Node* rightRotate(Node* y) {
        Node* x = y->left;
        Node* T2 = x->right;

        // Perform rotation
        x->right = y;
        y->left = T2;

        // Update heights
        y->height = max(height(y->left), height(y->right)) + 1;
        x->height = max(height(x->left), height(x->right)) + 1;

        return x;
    }

    // Perform a left rotation to balance the tree
    Node* leftRotate(Node* x) {
        Node* y = x->right;
        Node* T2 = y->left;

        // Perform rotation
        y->left = x;
        x->right = T2;

        // Update heights
        x->height = max(height(x->left), height(x->right)) + 1;
        y->height = max(height(y->left), height(y->right)) + 1;

        return y;
    }

    // Recursive function to insert a node and balance the tree
    Node* insertNode(Node* node, Course course) {
        // Standard BST insertion
        if (node == nullptr) return new Node(course);

        if (course.courseNumber < node->course.courseNumber) {
            node->left = insertNode(node->left, course);
        } else if (course.courseNumber > node->course.courseNumber) {
            node->right = insertNode(node->right, course);
        } else {
            return node; // Equal keys are not allowed
        }

        // Update the height of this ancestor node
        node->height = 1 + max(height(node->left), height(node->right));

        // Get the balance factor to check if it became unbalanced
        int balance = getBalance(node);

        // Left Left Case
        if (balance > 1 && course.courseNumber < node->left->course.courseNumber)
            return rightRotate(node);

        // Right Right Case
        if (balance < -1 && course.courseNumber > node->right->course.courseNumber)
            return leftRotate(node);

        // Left Right Case
        if (balance > 1 && course.courseNumber > node->left->course.courseNumber) {
            node->left = leftRotate(node->left);
            return rightRotate(node);
        }

        // Right Left Case
        if (balance < -1 && course.courseNumber < node->right->course.courseNumber) {
            node->right = rightRotate(node->right);
            return leftRotate(node);
        }

        return node;
    }

    // Recursive in-order traversal to print courses alphabetically
    void inOrderTraversal(Node* node) {
        if (node != nullptr) {
            inOrderTraversal(node->left);
            cout << node->course.courseNumber << ", " << node->course.courseTitle << endl;
            inOrderTraversal(node->right);
        }
    }

    // Recursive search function
    void searchNode(Node* node, string courseNumber) {
        if (node == nullptr) {
            cout << "Course " << courseNumber << " not found in the course list." << endl;
            return;
        }

        if (node->course.courseNumber == courseNumber) {
            cout << "Course Number: " << node->course.courseNumber << endl;
            cout << "Course Title: " << node->course.courseTitle << endl;

            if (node->course.prerequisites.empty()) {
                cout << "No prerequisites." << endl;
            } else {
                cout << "Prerequisites: " << endl;
                for (const string& prereq : node->course.prerequisites) {
                    cout << " * " << prereq << endl;
                }
            }
            return;
        }

        // Search left or right depending on alphanumeric value
        if (courseNumber < node->course.courseNumber) {
            searchNode(node->left, courseNumber);
        } else {
            searchNode(node->right, courseNumber);
        }
    }

    // Helper to safely delete all nodes and free memory
    void destroyTree(Node* node) {
        if (node != nullptr) {
            destroyTree(node->left);
            destroyTree(node->right);
            delete node;
        }
    }

public:
    AVLTree() : root(nullptr) {}

    // Destructor to prevent memory leaks
    ~AVLTree() {
        destroyTree(root);
    }

    void insert(Course course) {
        root = insertNode(root, course);
    }

    void printInOrder() {
        inOrderTraversal(root);
    }

    void search(string courseNumber) {
        searchNode(root, courseNumber);
    }
    
    bool isEmpty() {
        return root == nullptr;
    }
};

// Function to trim leading spaces
string trimLeadingSpaces(const string& str) {
    size_t start = 0;
    while (start < str.length() && (str[start] == ' ' || str[start] == '\t')) {
        ++start;
    }
    return str.substr(start);
}

// Function to trim trailing spaces
string trimTrailingSpaces(const string& str) {
    size_t end = str.length();
    while (end > 0 && (str[end - 1] == ' ' || str[end - 1] == '\t')) {
        --end;
    }
    return str.substr(0, end);
}

// Function to load course data and store it in the AVL Tree
void loadCourseData(const string& filename, AVLTree& tree) {
    ifstream file(filename);

    if (!file.is_open()) {
        cout << "Error: File not found or cannot be opened" << endl;
        return;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string courseNumber, courseTitle;
        vector<string> prerequisites;
        string prerequisite;

        getline(ss, courseNumber, ',');
        getline(ss, courseTitle, ',');

        courseNumber = trimTrailingSpaces(trimLeadingSpaces(courseNumber));
        courseTitle = trimTrailingSpaces(trimLeadingSpaces(courseTitle));

        while (getline(ss, prerequisite, ',')) {
            prerequisite = trimTrailingSpaces(trimLeadingSpaces(prerequisite));
            prerequisites.push_back(prerequisite);
        }

        if (courseNumber.empty() || courseTitle.empty()) {
            cout << "Error: Invalid line format. Each line must include course number and title." << endl;
            continue;
        }

        // Insert the formatted course object into the AVL tree
        tree.insert(Course(courseNumber, courseTitle, prerequisites));
    }

    file.close();
    cout << "Data loaded successfully from " << filename << endl;
}

void displayMenu() {
    cout << endl;
    cout << "1. Load Data Structure." << endl;
    cout << "2. Print Course List." << endl;
    cout << "3. Print Course." << endl;
    cout << "9. Exit" << endl;
}

int main() {
    AVLTree courseTree;
    string filename;
    int option;

    cout << "Welcome to the course planner." << endl;
    while (true) {
        displayMenu();
        cout << endl;
        cout << "What would you like to do? ";
        
        if (!(cin >> option)) {
            cout << "Invalid input. Please enter a valid number." << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            continue;
        }

        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        switch (option) {
        case 1:
            cout << "Enter the filename: ";
            getline(cin, filename);
            loadCourseData(filename, courseTree); 
            break;

        case 2:
            if (courseTree.isEmpty()) {
                cout << "No data loaded. Please load the data first." << endl;
            }
            else {
                cout << "Here is a sample schedule:" << endl << endl;
                courseTree.printInOrder(); 
            }
            break;

        case 3:
            if (courseTree.isEmpty()) {
                cout << "No data loaded. Please load the data first." << endl;
            }
            else {
                cout << "What course do you want to know about? ";
                string courseNumber;
                getline(cin, courseNumber);
                
                // Convert input to uppercase just in case user types lowercase
                for (auto & c: courseNumber) c = toupper(c);
                
                courseTree.search(courseNumber); 
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
