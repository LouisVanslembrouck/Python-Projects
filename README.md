# Description


1. An input .txt file is taken which has to be in the correct format ( Consult 'Input File' section on how to create correct input file ).
2. An SSH session is opened to the host
3. A combination of hostname, filename, and timestamp is used to look up the file.
4. The file is transferred through sftp using the existing SSH transport socket.
5. Both Connections are closed.
6. Steps 2 to 5 are repeated for each host.
7. An output file is generated in the current directory. !!! Please check for any failed files here !!!


# Input File


Use following query to retrieve the list of files to retrieve:

    Select Concat(Id, '.xml'), Hostname, RowCreationTimeStamp from [OBP-Archive].ticket.missingTicket where Hostname IS NOT NULL

Copy the output into the 'poslog.txt' file that is provided in the current directory. Overwrite any existing data in this file. Save the file.
!!! Verify if there are no trailing spaces or newlines !!!

1. Run the 'run.exe' file.
2. Select the 'poslog.txt' file through the file input button.
3. Click the 'Download' button.
4. Verify the output.txt file.
5. Check the /Copied folder that was created for the retrieved .xml files.


--- For questions or issues, please contact LVL ---
