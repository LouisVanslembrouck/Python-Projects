Description
An input .txt file is taken which has to be in the correct format ( Consult 'Input File' section on how to create correct input file ).
An SSH session is opened to the host
A combination of hostname, filename, and timestamp is used to look up the file.
The file is transferred through sftp using the existing SSH transport socket.
Both Connections are closed.
Steps 2 to 5 are repeated for each host.
An output file is generated in the current directory. !!! Please check for any failed files here !!!
Input File
Use following query to retrieve the list of files to retrieve:

Select Concat(Id, '.xml'), Hostname, RowCreationTimeStamp from [OBP-Archive].ticket.missingTicket where Hostname IS NOT NULL
Copy the output into the 'poslog.txt' file that is provided in the current directory. Overwrite any existing data in this file. Save the file. !!! Verify if there are no trailing spaces or newlines !!!

Run the 'run.exe' file.
Select the 'poslog.txt' file through the file input button.
Click the 'Download' button.
Verify the output.txt file.
Check the /Copied folder that was created for the retrieved .xml files.
--- For questions or issues, please contact LVL ---
