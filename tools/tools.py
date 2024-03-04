import pandas as pd
import numpy as np

version = 'Version'
maxchannels = 'Maxchannels'
sample_id = 'Sample ID'
vialnumber = 'Vial Number'
Volume = 'Volume'
time = 'Acquisition Date and Time'
sampling_rate = 'Sampling Rate'
TotalDataPoints = 'Total Data Points'
units = 'Y Axis Title'
multiplier_units = 'Y Axis Multiplier'
DF_DATA_POINTS = 'Data Points (mV)'
DF_TIME = 'Time (min)'
DF_CHANNEL = 'Acquisition Channel'


def open_file(path: str | bytearray, preamble_length: int = 16) -> (dict, pd.DataFrame):
    assert preamble_length > 0, 'Preamble length must be positive and greater than 0'

    directory = {
        version: None,
        maxchannels: None,
        sample_id: None,
        vialnumber: None,
        Volume: None,
        time: None,  # MM/DD/YYY H:MM:SS AM/PM
        sampling_rate: None,  # Hz
        TotalDataPoints: None,
        units: None,
        multiplier_units: None,
        # data: {},
    }

    # This way we can keep the directory
    data = {}

    with open(path, 'r') as file:
        lines = file.readlines()
        # if not any(elem is None for elem in variable_list):
        #     pass
        for n, line in enumerate(lines):
            # print(n, line.rstrip('\n'))
            for value in directory.keys():  # directory keys are named after the text in the line that has the data
                if value.lower() in line.lower():  # If the text is in the line
                    result = line[len(value)+1:].strip()  # we grab the stuff after the line, +1 for the colon
                    if value == sampling_rate:  # Remove superfluous text so we can convert the numbers later
                        result = result.rstrip('Hz')
                    if value == TotalDataPoints:  # Remove superfluous text so we can convert the numbers later
                        result = result.rstrip('Pts.')
                    result = result.strip().split('\t')  # Remove white space, split along tabs, results is now a list
                    try:  # Most values are stored as integer
                        result = [int(r) for r in result]
                    except ValueError:
                        try:  # Some are stored as float
                            result = [float(r) for r in result]
                        except ValueError:  # Probably text otherwise
                            pass
                    # Compress lists with one entry, this might turn out to be not smart later on
                    if len(result) == 1 and value != TotalDataPoints:
                        result = result[0]
                    directory[value] = result
                    break
            if n > preamble_length:  # Don't need to go further
                break

        # Let's check a few things
        assert directory[maxchannels] > 0, 'No acquisition channels provided'
        assert directory[maxchannels] == \
            len(directory[sampling_rate]) == \
            len(directory[TotalDataPoints]) == \
            len(directory[units]) == \
            len(directory[multiplier_units]), \
            f"Error parsing data file: some information is missing:\n{lines[:preamble_length+40]}"
        assert len(lines) == sum(directory[TotalDataPoints]) + preamble_length, \
            (f"Error: Missing data in file, could not account for all data points.\n"
             f"Expected: {int(sum(directory[TotalDataPoints]) + preamble_length)}\n"
             f"Received: {len(lines)}\n"
             f"Expected due to promised data points: {', '.join(str(int(i)) for i in directory[TotalDataPoints])} "
             f"and the preamble length of {preamble_length}\n{lines[:preamble_length+40]}")
        assert len(directory[TotalDataPoints]) > 0, 'No data points listed'

        pointer = 0
        for i in range(0, int(directory[maxchannels])):
            # Construct Data: from preamble to first data set, from there to next, and so on
            clist = lines[int(pointer + preamble_length):int(directory[TotalDataPoints][i] + preamble_length + pointer)]
            # Version 3 seems to always return int
            try:
                clist = [int(c.strip()) for c in clist]  # * directory[multiplier_units][i]
            except ValueError as exc:
                raise ValueError(f"Float in Data from file:\n{path}") from exc
            # Save in directory for dataframe construction
            data[i] = clist
            # print(f"{i}, {directory[TotalDataPoints][i]}, {pointer}")
            # Advance to next position
            pointer += directory[TotalDataPoints][i]
        # Check that we have the entire file loaded
        assert pointer + preamble_length == len(lines), "Error reading lines"
    # print(directory)

    # Create long form Dataframe
    df = None
    for n in range(0, int(directory[maxchannels])):
        c_df = pd.DataFrame(
            {
                DF_DATA_POINTS: data[n],
                # Convert Hz to min
                DF_TIME: [i / directory[sampling_rate][n] for i in range(0, int(directory[TotalDataPoints][n]))],
                DF_CHANNEL: n
            },
        )
        # Why ever this cannot be set during df construction is beyond me
        c_df = c_df.astype(
            dtype={
                DF_DATA_POINTS: np.float64,
                DF_TIME: np.float64,
                DF_CHANNEL: np.uint8,
            },
        )
        # Convert data to float
        c_df[DF_DATA_POINTS] = c_df[DF_DATA_POINTS] * directory[multiplier_units][n]

        # Concat if necessary
        if df is not None:
            df = pd.concat([df, c_df], ignore_index=True, axis='rows')
        else:
            df = c_df
    # print(df)
    # print(df.info())
    return directory, df
