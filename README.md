# version-1.0
Dejavu Forensics: version 1.0

## Simple Scenario: Binary classification

In the presented scenario, 1,000 (thousand) JPEG files and 1,000 (thousand) PNG files were designated, respectively considered class and counter-class. The files were cataloged on the world wide web.

The proposed work creates an authorial tool aiming at target class pattern recognition for JPEG files. From a training set, it is possible to formulate a hypothesis about the clusters of the target class (JPEG). It is up to the authorial system to estimate the class of an unprecedented cluster. It does this by comparing its features audited in real time and those obtained during the training stage.

## Complex Scenario: One-against-all method classification

In this scenario, a database was formed containing 16 thousand files, one thousand of each extension presented below.
The files were cataloged on the world wide web. The main objective of the experiment is to simulate a common user's computer. In contemporary times, electronic computers such as desktop computers, cell phones and other devices are not just focused on entertainment. They became indispensable for the fulfillment of domestic, professional, academic and planning tasks.

The hypothesis is that the authorial system is able to differentiate clusters of the target class (JPEG) from other types of files, even though they were not presented during its training phase. The one-against-all method is applied in this complex scenario. In statistical terms, it only matters the segregation of clusters of the target class to the detriment of all other classes.
After the collection, the following formatted data recovery tools are employed.

## Foremost

Foremost is a console software whose objective is to recover data formatted through Data Carving, considering the headers, footers and file structures, being able to work with image files or directly in a given unit.

-	-t: specifies the type of files to be recovered, 
for example,  JPEG, gif, png, bmp, 
or you can use all to recover all types of files.
-	-i: abbreviation for input, for the source partition.
-	-o: short for output, for the destination path of the files to be retrieved (on another partition such as an auxiliary memory device). By default foremost creates a folder named output, if the user does not define the destination.

In the console, we use Foremost:
-	  foremost -t all -i image.dd

## Scalpel

By default, all types of files are contained in the standard configuration file (systems/etc/scalpel/scalpel.conf files). \linebreak
This file contains comments that correspond to the configuration pattern. To specify which are the types of files to be extracted, it is necessary to uncomment the lines referring to the extensions of the files.

\begin{itemize}
	\item[\textcolor{ocre}{\textbullet}] 
The source partition. Note that there is no -i directive even though the Scalpel documentation states that it is required.
	\item[\textcolor{ocre}{\textbullet}] 
-o: short for output, for the destination path of the files to be retrieved. It is folder must first be created before Scalpel is invoked.
	\item[\textcolor{ocre}{\textbullet}] 
-c: configuration file discussed earlier.
At the console, we use Scalpel:
\begin{verbatim}
    scalpel image.dd -o /output2/ 
    -c /etc/scalpel/scalpel.conf
\end{verbatim}

\end{itemize}

## Magic Rescue
Magic Rescue also employs Data Carving to recover formatted data. By default, all types of files to be recovered are contained in:
(files systems/usr/share/magicrescue/recipes)

\begin{itemize}
	\item
-d: to the destination path of the files to be recovered.
It is necessary that the folder is created before Magic Rescue is invoked.
	\item
There is no flag(directive) for the source partition, just quote it in the command.
	\item
-r: configuration files discussed earlier.
In the console, use Magic Rescue:
\begin{verbatim}
    magicrescue -d output3 image.dd  -r avi 
    -r canon-cr2 -r elf -r flac  -r gpl -r gzip 
    -r jpeg-exif -r jpeg-jfif  -r mbox 
    -r mbox-mozilla-inbox  -r mbox-mozilla-sent 
    -r mp3-id3v1 -r mp3-id3v2 -r msoffice 
    -r nikon-raw -r perl -r png -r ppm 
    -r sqlite -r zip
\end{verbatim}
\end{itemize}

## Photorec

PhotoRec is an open source application. It has the function of recovering data that cannot be opened, and can be used on mobile devices such as pendrive, CDs and HDs.

## Recuva

Recuva allows you to recover files that have been deleted on Windows system. This recovery is not restricted to the hard disk, it also makes it possible to rescue files saved on portable devices. Its main function is to locate files that can be recovered. However, the program also allows a complete deletion of files.

## Autopsy

Autopsy makes it possible to recover deleted data.
Autopsy makes it possible to recover deleted data. With this tool, you cannot directly access the drive or image to perform Data Carving. You must follow the process of creating the case, building the preview file, the result files, analyzing the results, performing integrity checks, and extracting the data.


## DECA

DECA employs the libraries:


\begin{itemize}

\item 
libtsk-dev (sleuthkit): responsible for reading clusters from the target storage device.

\item
libmagic-dev: Data Carving manager (magic numbers).

\item
liblinear-dev: responsible for the pattern recognition step using linear discriminant.

\item
libsvm-dev: responsible for the pattern recognition step through Support Vector Machine.
\end{itemize}

The framework used as a basis is DECA, whose name stands for Decision Theory Sculpture \cite{gladyshev2017decision}. DECA employs corresponds to a Data Carving algorithm that combines magic numbers and cluster pattern recognition based on machine learning.
DECA is designed for fast recovery of unfragmented JPEG data. The process involves checking for the presence of JPEG data in clusters that are identified by reading the header and footer signatures. 
Based on DECA, the authoring algorithm goes beyond magic numbers. The authoring approach has a specific feature that concerns the identification of headers and footers. 
There is pattern recognition of JPEG files through machine learning.
In this sense, Support Vector Machine (SVM) corresponds to one of the Machine Learning methods that is very important in recognizing patterns in a complex data set \added{[14]}.

Introduced through the statistical theory of learning by Vapnik \cite{vapnik1999nature}. This classification is based on the principle of optimal separation between classes, the goal of SVM is to classify a data set by creating an optimal decision surface known as a hyperplane. This decision surface tends to optimize the classification accuracy over the training set by providing the best margins relative to the support vectors \cite{chang2011libsvm}. The expectation is that the best hyperplane will have a higher generalization ability when joined to the test set.

The authoring tool employs the following parameters:
\begin{itemize}
	\item 
-vv: abbreviation for \textit{verbose} in order to print on the screen the progress of the expertise.
	\item 
-o:  short for output, for the destination path of the files to be retrieved (on another partition such as an auxiliary memory device). It is necessary that the
folder must be created before the authoring tool is invoked.
    \item
There is no flag (directive) for the source partition, just quote it in the command.
	\item 
--deca: with machine learning added to the \textit{Data Carving}. 
	\item 
-m  jpeg.model: file containing the configuration parameters of the machine learning.
\item 
In the console, we use:
\begin{verbatim}
    ./deca -vv -o /home/kali/Desktop/output 
    --deca -m jpeg.model image.dd
\end{verbatim}
\end{itemize}
