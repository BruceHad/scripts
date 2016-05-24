# EDIFact Parser

## Edifact 

EDIFACT has a hierarchical structure.

The top level is referred to as an interchange, which is made up of segments, which contain composites/components, containing elements.

Segments are terminated by the single quote ' character. Components are seperated by the colon : character. And data elements are split by the + character.

The EDI files are complex and don't seem well formed, so parsing them may be tricky.

The following segments are part of the EDI file. Each file has the source (email address) on the first line, then has a single line containing the body of the message (no line breaks). Each message is wrapped by a single UNB and UNZ header and trailer segment, containing a sequence of segments for each claim in the message. So a UNH segment indicates the start of a new claim.

UNB	Interchange header			Wrapper
UNH	Message header				Claim
RFF	Reference					Claim
PNA	Party name					Claim
CED	Computer environment		Claim
PAT	Patient details				Claim
TDA	Treatments					Claim
CHX	Charges						Claim
TST	Tooth specific treatment	Claim
CUR	Claims under regulations	Claim
CHT	Dental chart				Claim
OBS	Observations				Claim
ENC	Enclosures					Claim
RPA	Request for prior approval	Claim
UNT	Message trailer				Claim
UNZ	Interchange trailer			Wrapper