import json
import os
import sys
import pandas
from datetime import datetime, date, time

def split_into_files(input_filename,output_filename):
    napa_df = pandas.read_table('Data/Geo/napa_coordinates.txt', sep=",", names=('lat', 'long'))

    with open(input_filename, "r") as input:
        line = input.readline()
        cnt = 1
        while line:
            with open(output_filename+str(int(cnt/2500))+".txt", "a+", encoding='UTF-8') as output:
                if(cnt==1 or cnt%2500==0):
                    output.write("day\tmonth\tyear\thour\tminute\tsecond\tlat\tlong\ttweet\tcategory\n")
                fields = line.split("\t")
                json_text = json.loads(fields[0])
            
                created_at_txt = json_text["created_at"]
                dt = datetime.strptime(created_at_txt, "%a %b %d %H:%M:%S  %z  %Y")
                day = dt.strftime("%d")
                month = dt.strftime("%m")
                year = dt.strftime("%Y")
                hour = dt.strftime("%H")
                minute = dt.strftime("%M")
                second = dt.strftime("%S")
                lat = napa_df["lat"][cnt-1]
                longitude = napa_df["long"][cnt-1]
                tweet = json_text["text"].replace("\r"," ")
                tweet = tweet.replace("\n"," ")
                category=""
                if(len(fields)>1):
                    category = fields[1]
                #print(date_str+"\t"+time_str+"\t"+json_text["text"])

                output.write(day+"\t"+month+"\t"+year+"\t"+hour+"\t"+minute+"\t"+second+"\t"+str(lat)+"\t"+str(longitude)+"\t"+tweet+"\t"+category+"\n")
                with open(output_filename+"_all.txt", "a+", encoding='UTF-8') as output:
                    if(cnt==1):
                        output.write("day\tmonth\tyear\thour\tminute\tsecond\tlat\tlong\ttweet\tcategory\n")
                    output.write(day+"\t"+month+"\t"+year+"\t"+hour+"\t"+minute+"\t"+second+"\t"+str(lat)+"\t"+str(longitude)+"\t"+tweet+"\t"+category+"\n")
                with open(output_filename+"_classes_all.txt", "a+", encoding="UTF-8") as output:
                    output.write(category+"\t"+tweet+"\n")
            line = input.readline()
            cnt += 1

# if we're running this as a script
if __name__ == '__main__':
    # get tweets for username passed at command line
    if len(sys.argv) == 3:
        split_into_files(sys.argv[1],sys.argv[2])
    else:
        print("Error")



        # '\t'+year+'\t'+hour+'\t'+minute+'\t'+second+'\t'+str(lat)+'\t'+str(longitude)+'\t'+tweet+'\t'+category+'\n'
    #     output.write(line)
    # with open(output_filename+"_classes_all.csv", "a+", encoding='UTF-8') as output:
    #     if(len(fields)>1):
    #         output.write(category+"\t"+tweet+"\n")
    #     else:
    #         output.write(tweet+"\n")
    # print(tweets_all_df)
    # print("=====================")
    # print(tweets_all_classes_df)
#
#     tweets_all_df.to_csv(output_filename + "_all.txt", sep='\t', index=False)
#     tweets_all_classes_df.to_csv(output_filename + "_classes_all.txt", header=None, index=False)
#     # print('complete')
#
#
# # if we're running this as a script
# if __name__ == '__main__':
#     # get tweets for username passed at command line
#     if len(sys.argv) == 4:
#         split_into_files(sys.argv[1], sys.argv[2], sys.argv[3])
#     else:
#         print("Error")     # print("=====================")
#     # print(tweets_all_classes_df)
#
    # tweets_all_df.to_csv(output_filename + "_all.txt", sep='\t', index=False)
    # tweets_all_classes_df.to_csv(output_filename + "_classes_all.txt", header=None, index=False)
#     # print('complete')
#
#
# # if we're running this as a script
# if __name__ == '__main__':
#     # get tweets for username passed at command line
#     if len(sys.argv) == 4:
#         split_into_files(sys.argv[1], sys.argv[2])
#     else:
#         print("Error")