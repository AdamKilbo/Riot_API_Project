/* Example of FILE I/0
   From www.cplusplus.com/reference/clibrary/cstdio/FILE/  
   Modified to use getline(), 10/2015*/

#include <stdio.h>

int main()
{
   FILE *pFile;
   char *buffer = NULL;
   size_t bufflen = 0; 

   pFile = fopen("myfile.txt", "r");
   if (pFile == NULL) 
     perror ("Error opening file");
   else {
     while (getline(&buffer, &bufflen, pFile) >= 0)
       fprintf(stdout, "%s", buffer);
     fclose(pFile);
   }
   return 0;
}
