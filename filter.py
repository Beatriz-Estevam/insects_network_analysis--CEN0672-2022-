import pandas as pd

# loading database file
all_data = pd.read_csv(
    '/home/bia/insects_network_analysis--CEN0672-2022-/\
0183649-220831081235567.csv', on_bad_lines='skip', sep="\t")

''' Mmanipulating GBIF database to keep only sites with more than one observations and observed more than once
    same site = same location (same Longitude and Latitude'''


# making a subset of database files keeping only the interest columns
interest_columns = all_data[['gbifID', 'order', 'species', 'decimalLatitude',
                             'decimalLongitude', 'eventDate',
                            'day', 'month', 'year']]
# print(interest_columns)

# Removing duplicated rows, because it will not work with adundance data
df = interest_columns.drop_duplicates(subset=(['order', 'species', 'decimalLatitude',
                                               'decimalLongitude', 'eventDate',
                                               'day', 'month', 'year']))

# removing lines without info in at least one of the interest columns
# dropna = remove rows without info
complete_lines = df.dropna()
# print(complete_lines)

# Keep only lines with Latitude and Longitude duplicated (e.g. more than one observation in a site)
# and with different data.
df = complete_lines.loc[complete_lines.duplicated(
    subset=['decimalLatitude', 'decimalLongitude', 'eventDate'], keep=False)]
# print(df)

# Subseting by place (Latitude and Longitude equal) and different time:
latitudes = []
for latitude in df['decimalLatitude']:
    # print(latitude)
    if latitude not in latitudes:
        latitudes.append(latitude)

        # latitude = -10.294167

        latitude_df = df.loc[df['decimalLatitude'] == latitude]
        # print(latitude_df)

        if len(latitude_df.eventDate.drop_duplicates().tolist()) > 19:
            diff_date_df = latitude_df
            # print(diff_date_df)

            if not diff_date_df[diff_date_df.duplicated("species")].empty:
                # print(diff_date_df[diff_date_df.duplicated("species")])
                species_duplicated_df = diff_date_df
                print(species_duplicated_df)

                file_name = f'grupo_{latitude}.csv'

                species_duplicated_df = species_duplicated_df[[
                    'species', 'eventDate']]
                species_date_dict = species_duplicated_df.values.tolist()
                # print(species_date_dict)

                dict_to_csv = {}
                for dupla in species_date_dict:
                    if dupla[0] not in dict_to_csv.keys():
                        dict_to_csv[dupla[0]] = [dupla[1]]
                    else:
                        if dupla[1] not in dict_to_csv[dupla[0]]:
                            dict_to_csv[dupla[0]].append(dupla[1])
                # print(dict_to_csv)

                locals = species_duplicated_df.drop_duplicates(
                    subset=["eventDate"])
                date_list = locals.eventDate.values.tolist()
                # print(date_list)

                to_csv = []
                speci = []
                for spp in dict_to_csv.keys():
                    speci.append(spp)
                    csv_dicta = {}
                    csv_dicta['espécie'] = spp
                    for data in date_list:
                        if data in dict_to_csv[spp]:
                            csv_dicta[data] = "1"
                        else:
                            csv_dicta[data] = "0"
                    # print(csv_dicta)
                    to_csv.append(csv_dicta)
                # print(to_csv)

                dframe = pd.DataFrame(to_csv)
                dframe = dframe.set_index('espécie')
                dframe.to_csv(file_name, index=True, header=True)
