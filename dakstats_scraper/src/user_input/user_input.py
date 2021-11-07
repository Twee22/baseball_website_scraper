def get_user_input():
    school_name = input("Enter the name of the school that you want to scrape. If you want all available schools, leave this empty.\n")
    year = input("Enter the year that you want to scrape. If you want all available years, leave this empty.\n")

    user_input = {"school_name": school_name, "year": year}

    return user_input