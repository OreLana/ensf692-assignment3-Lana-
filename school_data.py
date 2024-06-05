# school_data.py
# Author Name: Oreoluwa Lana
#
# A terminal-based application for computing and printing statistics based on given input.
# You must include the main listed below. You may add your own additional classes, functions, variables, etc. 
# You may import any modules from the standard Python library.
# Remember to include docstrings and comments.


import numpy as np
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022

# Declare any global variables needed to store the data here


# You may add your own additional classes, functions, variables, etc.

# School data dictionary
school_dict = {
    1224: "Centennial High School",
    1679: "Robert Thirsk School",
    9626: "Louise Dean School",
    9806: "Queen Elizabeth High School",
    9813: "Forest Lawn High School",
    9815: "Crescent Heights High School",
    9816: "Western Canada High School",
    9823: "Central Memorial High School",
    9825: "James Fowler High School",
    9826: "Ernest Manning High School",
    9829: "William Aberhart High School",
    9830: "National Sport School",
    9836: "Henry Wise Wood High School",
    9847: "Bowness High School",
    9850: "Lord Beaverbrook High School",
    9856: "Jack James High School",
    9857: "Sir Winston Churchill High School",
    9858: "Dr. E. P. Scarlett High School",
    9860: "John G Diefenbaker High School",
    9865: "Lester B. Pearson High School"
}

class School:
    """A class representing a school and its enrollment data."""

    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.index = list(school_dict.keys()).index(self.code)

    def print_school_details(self):
        """Prints the school's details."""
        print(f"School Name: {self.name}, School Code: {self.code}")

    def calc_school_statistics(self, grade_10_data, grade_11_data, grade_12_data):
        """
        Calculates the different statistics for the specific school given the name and code.
        Parameters:
            grade_10_data (np.array): The enrollment data for grade 10.
            grade_11_data (np.array): The enrollment data for grade 11.
            grade_12_data (np.array): The enrollment data for grade 12.
        Returns:
            dictionary: A dictionary containing the statistics.
        """
        # Concatenate enrollment data for all grades into a single array
        all_enrollments = np.concatenate((grade_10_data[:, self.index], grade_11_data[:, self.index], grade_12_data[:, self.index]))

        # Create a mask to filter enrollments greater than 500
        mask = all_enrollments > 500
        greater_than_500 = all_enrollments[mask]

        # Calculate the median enrollment for enrollments greater than 500, or 0 if none exist
        check_enrollment_number = np.nanmedian(greater_than_500) if greater_than_500.size > 0 else 0

        # Calculate total enrollment for each year
        total_enrollments = {}
        for year in range(2013, 2023):
            total_enrollments[year] = np.nansum([grade_10_data[year - 2013, self.index], grade_11_data[year - 2013, self.index], grade_12_data[year - 2013, self.index]])

        # Calculate mean total enrollment over ten years
        yearly_totals = list(total_enrollments.values())
        mean_total_enrollment = np.nanmean(yearly_totals)

        # Return a dictionary containing the calculated statistics
        return {
            "grade_10_mean": np.nanmean(grade_10_data[:, self.index]), #mean grade for grade 10 of the school 
            "grade_11_mean": np.nanmean(grade_11_data[:, self.index]), #mean grade for grade 11 of the school 
            "grade_12_mean": np.nanmean(grade_12_data[:, self.index]), #mean grade for grade 11 of the school 
            "highest_enrollment_single_grade" : np.nanmax(all_enrollments), # Highest enrollment among all grades
            "lowest_enrollment_single_grade": np.nanmin(all_enrollments), # Lowest enrollment among all grades
            "total_ten_year_enrollment": np.nansum(all_enrollments), #Total enrollment over ten years
            "check_enrollment_number": check_enrollment_number, # Median enrollment for enrollments greater than 500
            "total_enrollments": total_enrollments, # Total enrollment for each year
            "mean_total_ten_year_enrollment": mean_total_enrollment # Mean total enrollment over ten years
        } 


def get_user_input():
    """Gets user input for the school name or code and returns the corresponding data."""
    while True:
        try:
            given_input = input("Please enter the high school name or code: ")
            if given_input.isdigit():
                code = int(given_input)
                if code in school_dict:
                    return {"name": school_dict[code], "code": code}
                else:
                    raise ValueError("You must enter a valid school name or code.")
            else:           
                found_school = False
                for code, name in school_dict.items():
                    if name.lower() == given_input.lower():
                        found_school = True
                        return {"name": name, "code": code}
                if not found_school:
                    raise ValueError("You must enter a valid school name or code.")
        except ValueError as e:
            print(e)

def calc_general_statistics(grade_10_data, grade_11_data, grade_12_data):
    """
    Calculates general statistics for all schools based on enrollment data for grade 10, grade 11, and grade 12.

    Parameters:
        grade_10_data (np.array): Enrollment data for grade 10.
        grade_11_data (np.array): Enrollment data for grade 11.
        grade_12_data (np.array): Enrollment data for grade 12.

    Returns:
        dict: A dictionary containing general statistics.
    """
    all_enrollments = np.array([[grade_10_data],[grade_11_data],[grade_12_data]])

    # Initialize dictionaries to store statistics
    total_enrollments_grad_class = {}
    mean_enrollments = {}

    # Loop through each year and calculate statistics
    for year in range(2013, 2023):
        # Calculate total enrollment for the graduating class of each year
        total_enrollments_grad_class[year] = np.nansum([grade_12_data[year - 2013, :]])

        # Calculate mean enrollment for each year across all grades
        mean_enrollments[year] = np.nanmean([grade_10_data[year - 2013, :], grade_11_data[year - 2013, :], grade_12_data[year - 2013, :]])

    # Return a dictionary containing the calculated statistics
    return {
        "highest_enrollment_single_grade": np.nanmax(all_enrollments),
        "lowest_enrollment_single_grade": np.nanmin(all_enrollments),
        "total_year_enrollment_grad_class": total_enrollments_grad_class,
        "mean_year_enrollment": mean_enrollments   
    }


def main():
    print("\nENSF 692 School Enrollment Statistics\n")

    # Print Stage 1 requirements here

    # Stack grades data into a 3D array
    data_3d = np.stack((year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022))
    data_3d = data_3d.reshape(10,20,3)

    print(f"Shape of full data array: {data_3d.shape}")
    print(f"Dimensions of full data array: {data_3d.ndim}")

    # Extracting grade 10 enrollment data from the 3D array
    grade_10_data = data_3d[:, :, 0]

    # Extracting grade 11 enrollment data from the 3D array
    grade_11_data = data_3d[:, :, 1]

    # Extracting grade 12 enrollment data from the 3D array
    grade_12_data = data_3d[:, :, 2]

    # Print Stage 2 requirements here
    try: 
        school_info = get_user_input()

        school = School(school_info["name"], school_info["code"])

        print("\n***Requested School Statistics***\n")

        school.print_school_details()

        school_statistics = school.calc_school_statistics(grade_10_data, grade_11_data, grade_12_data)

        print(f"Mean enrollment for Grade 10: {int(school_statistics['grade_10_mean'])}")

        print(f"Mean enrollment for Grade 11: {int(school_statistics['grade_11_mean'])}")

        print(f"Mean enrollment for Grade 12: {int(school_statistics['grade_12_mean'])}")

        print(f"Highest enrollment for a single grade: {int(school_statistics['highest_enrollment_single_grade'])}")

        print(f"Lowest enrollment for a single grade: {int(school_statistics['lowest_enrollment_single_grade'])}")

        for year in range(2013, 2023):
            print(f"Total enrollment for {year}: {int(school_statistics['total_enrollments'][year])}")

        print(f"Total ten year enrollment : {int(school_statistics["total_ten_year_enrollment"])}")

        print(f"Mean total enrollment over 10 years: {int(school_statistics["mean_total_ten_year_enrollment"])}")

        if school_statistics["check_enrollment_number"] != 0:
            print(f"For all enrollments over 500, the Median value is: {int(school_statistics["check_enrollment_number"])}")
        else:
            print("No enrollments over 500.")
    except ValueError as e:
        print(e)


    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")

    general_statistics = calc_general_statistics(grade_10_data, grade_11_data, grade_12_data)

    print(f"Mean enrollment for 2013: {int(general_statistics["mean_year_enrollment"][2013])}")

    print(f"Mean enrollment for 2022: {int(general_statistics["mean_year_enrollment"][2022])}")

    print(f"Total graduating class of 2022: {int(general_statistics["total_year_enrollment_grad_class"][2022])}")

    print(f"Highest enrollment for a single grade: {int(general_statistics["highest_enrollment_single_grade"])}")

    print(f"Lowest enrollment for a single grade: {int(general_statistics["lowest_enrollment_single_grade"])}")


if __name__ == '__main__':
    main()

