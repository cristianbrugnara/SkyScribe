from sky_scribe.sky_scribe import *


if __name__ == '__main__':
    print(f"All available stations: ")
    print(get_all_stations_data())
    print()

    print("Once we know which stations are present, we can obtain their specific data by providing the id or the location.")
    print(f"Data of specific station: ")
    print(get_one_station_data(0))
    print()
    print("\n---------------------------------------------------------\n")

    print("Use the found ID to obtain a WeatherStation object.")
    lugano_station = get_one_station(0)
    print(lugano_station)

    print(f"Access its ID and location: {lugano_station.id}, {lugano_station.location}")
    print()
    print("\n---------------------------------------------------------\n")
    print(f"Each function that returns some samples can do it in form of:")
    print(f"* Sample objects (default)")
    print(f"* Dictionaries")
    print(f"* Dataframe rows\n\n")
    print("Get all measurements stored in the station (showing the first 3):\n ")
    all_samples = lugano_station.get_all_samples()
    for el in all_samples[:3]:
        print(el)
    print()
    print(lugano_station.get_all_samples(as_dict=True)[:3])
    print(lugano_station.get_all_samples(as_dataframe=True).head(3))
    print()
    print("\n---------------------------------------------------------\n")
    print(f"Get one specific sample by passing year, month, day, hour and minute; most method allow to either do this "
          f"or provide an already built datetime object, buildable with SkyScribe.build_date().\n")
    print(lugano_station.get_one_sample(2023,11,12,18,3))

    # using a prebuilt date
    date_1 = build_date(2023,11,12,18,3)

    # print(lugano_station.get_one_sample(prebuilt_date=date_1))

    print("\n---------------------------------------------------------\n")
    print("Get samples within a specified date range. Using the prebuild-date approach is suggested.\n")
    date_2 = build_date(2023,11,12,20,1)
    print(lugano_station.get_range_of_samples(prebuilt_date_1=date_1, prebuilt_date_2=date_2,as_dataframe=True))
    print()
    print("If we don't specify dates, all samples will be found.")
    print(f"Number obtained using get_all_samples(): {len(all_samples)}")
    print(f"Number obtained using get_range_of_samples(): {len(lugano_station.get_range_of_samples())}")
    print("\n---------------------------------------------------------\n")
    print("Get samples by filtering parameters (check documentation for the available parameters). ")
    print("The filtering syntax is: parameter=(min_value, max_value)")
    print("\nNow searching for samples with temp_c in [4.75, 10.565] and humidity in [29, 64]")
    filtered = lugano_station.get_filtered_samples(temp_c=(4.75,10.565), humidity=(29, 64))
    print(f"{len(filtered)} samples found, with the following max and min values.")
    temp_filtered = [el.temp_c for el in filtered]
    humid_filtered = [el.humidity for el in filtered]
    print(f"Temp_c | min: {min(temp_filtered)} | max: {max(temp_filtered)}")
    print(f"Humidity | min: {min(humid_filtered)} | max: {max(humid_filtered)}")
    print()
    print("Giving None values as boundaries means that no filtering will be applied there.")
    filtered2 = lugano_station.get_filtered_samples(temp_c=(4.75,None))
    temp2_filtered = [el.temp_c for el in filtered2]
    print()
    print(f"{len(filtered2)} samples found, with the following max and min values.")
    print(f"Temp_c | min: {min(temp2_filtered)} | max: {max(temp2_filtered)}")
    # Note that the min value is different since we don't have the same samples due to the humidity filter
    print()
    print("\n---------------------------------------------------------\n")
    sample_data = lugano_station.get_one_sample(prebuilt_date=date_1,as_dict=True)
    print("Deleting a sample.\n")
    lugano_station.delete_sample(prebuilt_date=date_1)

    try:
        lugano_station.get_one_sample(prebuilt_date=date_1)
    except NotFoundError:
        print(f"The sample doesn't exist anymore!\n")
    print("\n---------------------------------------------------------\n")
    print("Let's add it back! We can add samples as long as the date isn't already present."
          "\nHere we're using keyword arguments to rebuild it with its original data, but we can simply specify what we want: <parameter>=<value>\n")
    lugano_station.add_sample(prebuilt_date=date_1, **sample_data)
    print(lugano_station.get_one_sample(prebuilt_date=date_1))
    print()
    print("\n---------------------------------------------------------\n")
    print("Replacing a sample: meaning that after selecting a given date that sample will be replaced with another one.")
    print("We can obtain the same result with a delete_sample() followed by an add_sample().")
    print(f"Let's set temp_c to 60000 and rssi to -200!")
    lugano_station.replace_sample(prebuilt_date=date_1, temp_c = 60000, rssi = -200)
    print()
    print(lugano_station.get_one_sample(prebuilt_date=date_1))

    # we can use it also to revert the change
    lugano_station.replace_sample(prebuilt_date=date_1, **sample_data)
    print("\n---------------------------------------------------------\n")
    print()
    print("If we simply want to update ot correct a sample, instead of re-creating it from scratch, we can use update_sample().")
    print("Let's set rain_mm to 1.2345!")
    print()

    lugano_station.update_sample(prebuilt_date=date_1, field_to_update='rain_mm',value=1.2345)
    print(lugano_station.get_one_sample(prebuilt_date=date_1))

    lugano_station.update_sample(prebuilt_date=date_1, field_to_update='rain_mm', value=sample_data['rain_mm'])
    print()
    print("\n---------------------------------------------------------\n")
    print("STATISTICS")
    print("We can obtain all statistics for each field of our station data.")
    print()
    print(lugano_station.get_general_statistics(as_dataframe=True))
    print()
    print("Choose a specific statistic to compute.")
    print("Let's see the statistics of rain_mm!\n")
    print(f"Mean: {lugano_station.mean('rain_mm')}")
    print(f"Min: {lugano_station.min('rain_mm')}")
    print(f"Max: {lugano_station.max('rain_mm')}")
    print(f"Standard deviation: {lugano_station.std('rain_mm')}")
    print()
    print("\n---------------------------------------------------------\n")
    print("We can do the same things we just did on a certain date range.")
    print("The functions were separated to avoid cluttering too many arguments within a single simple stats function.")
    print()
    print(lugano_station.get_general_statistics_in_range(as_dataframe=True,prebuilt_date_1=date_1,prebuilt_date_2=date_2))
    print()
    print(f"Statistics of rain_mm from {date_1} to {date_2}:")
    print()
    print(f"Mean: {lugano_station.mean_in_range('rain_mm',prebuilt_date_1=date_1,prebuilt_date_2=date_2)}")
    print(f"Min: {lugano_station.min_in_range('rain_mm',prebuilt_date_1=date_1,prebuilt_date_2=date_2)}")
    print(f"Max: {lugano_station.max_in_range('rain_mm',prebuilt_date_1=date_1,prebuilt_date_2=date_2)}")
    print(f"Standard deviation: {lugano_station.std_in_range('rain_mm',prebuilt_date_1=date_1,prebuilt_date_2=date_2)}")
    print()
    print("\n---------------------------------------------------------\n")
    # PLOTS
    print("Be sure to check out the plot functions!")
    # The following function can all produce and download uni-variate graphs.
    # To see the graphs go into /images_saved
    img_path = 'images_saved'
    lugano_station.boxplot(field='temp_c', file_path=img_path)
    lugano_station.histogram(field='temp_c', file_path=img_path)
    lugano_station.lineplot(field_1='temp_c', file_path=img_path)  # if we don't specify a field_2, we'll only have one line

    # The next ones can produce graphs with two variables.
    lugano_station.lineplot(field_1='temp_c', field_2='humidity', file_path=img_path)
    lugano_station.scatterplot(field_1='temp_c', field_2='humidity', file_path=img_path)
    print("\n---------------------------------------------------------\n")

    print("FORECASTING")
    print("The first step is to instanciate a model using create_model().")
    print("The aim of the following functions and classes is to hide the complexity of creating a model and training it with Tensorflow.")
    print("This is why in the create_model() method we need to specify the information regarding our inputs and outputs. They can't be directly touched after.")
    model = lugano_station.create_model(input_fields=None, output_fields=['temp_mp1', 'humidity'], input_steps=20, horizon_steps = 3)
    print("The input and output fields are the column we want to use for training the model and to predict, respectively. When left None, all columns will be used for that particular task.")
    print("The input steps are the number of measurements the model uses to make a prediction, and the horizon steps represent the number of measurements of the prediction.")
    print("A more informed person can also specify optimizer and loss functions by using keras strings.")
    print()
    print(model)
    print("\n---------------------------------------------------------\n")

    print("Now we need to train the model.")
    print("This is simple: we just have to specify the number of epochs and the batch size (or leave default) in the train() method.")
    print()
    model.train(epochs=1,batch_size=128)

    print("\n---------------------------------------------------------\n")
    print("Now we can get our predictions!")
    preds = model.forecast(as_dataframe=True)
    print(preds)
    print("\n---------------------------------------------------------\n")
    print("We can also update the fields our model will be using (we would need to retrain after tough).")
    print("Updating input_fields to temp_c and output_fields to rssi.")
    model.update_model_fields(input_fields=['temp_c'],output_fields=['rssi'])

    idx = model.id

    print("\n---------------------------------------------------------\n")
    print("Lastly we can delete our models.\n")
    lugano_station.delete_model(idx)
    print()
    print(f"Models: {lugano_station.models}")
