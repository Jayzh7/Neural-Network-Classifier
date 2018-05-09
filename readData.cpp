// Read the sensor events from the input file, fp.  Associate the event
// with the corresponding activities.
void ReadData(FILE *fp)
{
	char *cptr, buffer[256], status[80];
	char date[80], time[80], sensorid[80], sensorvalue[80], alabel[80];
	int i, sole, length, num, same, previous;

	same = 0;                                        // New or continued activity
	sole = 0;
	previous = 0;
	cptr = fgets(buffer, 256, fp);
	while (cptr != NULL)
	{
		strcpy(alabel, "none");
		length = strlen(cptr);
		// Ignore lines that are empty or commented lines starting with "%"
		if ((length > 0) && (cptr[0] != '%'))
		{
			// Remove white space at the end of the line
			while ((length > 1) &&
				((cptr[length - 2] == ' ') || (cptr[length - 1] == '	')))
				length--;
			// There is a label if the line ends with " begin" or " end"
			if (((cptr[length - 4] == 'e') && (cptr[length - 3] == 'n') &&
				(cptr[length - 2] == 'd')) ||
				((cptr[length - 6] == 'b') && (cptr[length - 5] == 'e') &&
					(cptr[length - 4] == 'g') && (cptr[length - 3] == 'i') &&
					(cptr[length - 2] == 'n')))
			{
				sscanf(cptr, "%s %s %s %s %s %s",
					date, time, sensorid, sensorvalue, alabel, status);
			}
			else
			{
				sscanf(cptr, "%s %s %s %s %s",
					date, time, sensorid, sensorvalue, alabel);
				if (strcmp(alabel, "none") != 0)       // There is an activity label
					sole = 1;
			}

			if (sole == 1)              // A label is provided with no begin or end
			{
				num = FindActivity(alabel);
				if (open[num] == 1)                 // Add event to activity if open
				{
					AddActivity(date, time, sensorid, sensorvalue,
						num, 0, same, previous);
				}
				else                                           // Singleton activity
				{
					AddActivity(date, time, sensorid, sensorvalue,           // begin
						num, 1, same, previous);
					AddActivity(date, time, sensorid, sensorvalue,             // end
						num, 1, same, previous);
					previous = num;
				}
				sole = 0;
			}
			else if (strcmp(alabel, "none") == 0)                       // No label
			{
				if (same > 0)                   // Continue with previous activities
				{
					for (i = 0; i<numactivities; i++)   // Check for current activities
					{
						if (open[i] == 1)
							AddActivity(date, time, sensorid, sensorvalue,
								i, 0, same, previous);
					}
				}
			}
			else                       // There is an activity label for this event
			{
				num = FindActivity(alabel);
				same = AddActivity(date, time, sensorid, sensorvalue,
					num, 1, same, previous);
				if (same == 0)                 // Finished activity, update previous
					previous = num;
				for (i = 0; i<numactivities; i++)// Check for other current activities
				{
					if ((i != num) && (open[i] == 1))
						AddActivity(date, time, sensorid, sensorvalue,
							i, 0, same, previous);
				}
			}
		}

		cptr = fgets(buffer, 256, fp);                           // Get next event
	}
	for (i = 0; i<numactivities; i++)        // Output warning if activity not used
		if (afreq[i] == 0)
			printf("Activity %s is not found in the data\n", activitynames[i]);
}

// Return index that corresponds to the activity label.  If the label is not
// found in the list of predefined activity labels then an error is generated
// and the program is terminated.
int FindActivity(char *name)
{
	int i;

	for (i = 0; i<numactivities; i++)
		if (strcmp(name, activitynames[i]) == 0)
			return(i);

	printf("Unrecognized activity label %s\n", name);
	exit(1);
}


// Add the current sensor event to the sensor event sequence for a
// particular activity.
int AddActivity(char *date, char *time, char *sensorid, char *sensorvalue,
	int activity, int label, int same, int previous)
{
	int occurrence, length;

	occurrence = afreq[activity];
	length = lengthactivities[activity][occurrence];
	if (evnum < MAXALENGTH)
	{
		ProcessData(activity, occurrence, length, date, time,
			sensorid, sensorvalue);
		lengthactivities[activity][occurrence] += 1;
	}
	else
	{
		printf("Event %s %s %s %s\n", date, time, sensorid, sensorvalue);
		printf("Activity length for %s exceeds maximum\n",
			activitynames[activity]);
	}

	if ((label == 1) && (open[activity] == 0))         // Starting a new activity
	{
		open[activity] = 1;
		previousactivity[activity][occurrence] = previous;
		starts[activity][occurrence] = evnum - 1;
		return(same + 1);
	}
	else if (label == 0)                            // Continue existing activity
		return(same);
	else                                                       // Finish activity
	{
		afreq[activity] += 1;
		open[activity] = 0;
		// Make room for the next activity occurrence
		starts[activity] = (int *)realloc(starts[activity],
			(afreq[activity] + 1) * sizeof(int));
		lengthactivities[activity] = (int *)realloc(lengthactivities[activity],
			(afreq[activity] + 1) * sizeof(int));
		previousactivity[activity] = (int *)realloc(previousactivity[activity],
			(afreq[activity] + 1) * sizeof(int));
		lengthactivities[activity][afreq[activity]] = 0;
		previousactivity[activity][afreq[activity]] = 0;
		starts[activity][afreq[activity]] = 0;
		return(same - 1);
	}
}