def load_data(file_path):
    """
    load data from the specified file path

    Args:
        file_path (str): The path to the file containing the data

    Returns:
        pd.DataFrame: A pandas DataFrame containing the loaded data
    """
    import pandas as pd
    try:
        data = pd.read_csv(file_path) 
        print(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading from {file_path}: {e}")
        return None


