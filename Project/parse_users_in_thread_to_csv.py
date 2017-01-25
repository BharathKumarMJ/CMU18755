#!/usr/bin/python                                                               

# Load the JSON module and use it to load your JSON file.                       
# I'm assuming that the JSON file contains a list of objects.                   
import json
import csv
import wget
import time
import unicodedata

# Max depth to which you are allowed to go inside threads
max_depth = 0
# Starting depth
depth = 0
old_url = ""
user_names = set()
num_retries = 0
num_threads = 0
num_comments = 0
thread_id = 'T'
current_comment = 'C'

# Parses the given thread for users, author, and comments and outputs the names
# into two different files, one is the users.csv file which has the user names,
# other is the connections.csv file which has the edges between the nodes
def parse_thread_for_users(commenter_thread_obj, author, comment_number):
   # Builds a csv with two entires in each row
   # The two entires specify which user has commented on which other user
   # Representing the users as nodes, we can connect all the users                                                    
   global user_names
   global thread_id
   global num_comments
   global current_comment
   csv_file = open("connections.csv", 'a')              
   writer = csv.writer(csv_file)
   user_csv = open("users.csv", 'a')              
   user_writer = csv.writer(user_csv)
   for commentor in commenter_thread_obj["data"]["children"]:
      if commentor["kind"] == "more":
         continue
      commentor_name = commentor["data"]["author"]
      start_time = commentor["data"]["created"]
      #print author + "->" + commentor_name
      if author not in user_names:
         user_writer.writerow( [author] )
         user_names.add(author)
         writer.writerow( (author, comment_number, start_time) )

      if commentor_name not in user_names:
         user_names.add(commentor_name)
         user_writer.writerow( [commentor_name] )

      writer.writerow( (commentor_name, author, start_time) )
      writer.writerow( (commentor_name, thread_id, start_time) )

      user_writer.writerow( [current_comment] )
      num_comments += 1
      current_comment = 'C'+str(num_comments)
      writer.writerow( (commentor_name, current_comment, start_time) )      
      writer.writerow( (current_comment, comment_number, start_time) )      
      if ("replies" in commentor["data"]) and (commentor["data"]["replies"] != ""):
         parse_thread_for_users(commentor["data"]["replies"], commentor_name, current_comment)
   csv_file.close()
   user_csv.close()

# Function which parses the url and gets all valid urls from this particular user's 
# data. Called for each top level user
def get_valid_urls(url):
   global depth
   global old_url
   global num_retries
   global thread_id
   try:
      filename = wget.download(url.encode('ascii','ignore'), "tmp/userdata.json")
      user_data  = json.load(open(filename))
      if "error" in user_data:
         time.sleep(5)
         num_retries+=1
         if num_retries > 2:
            num_retries = 0
            return
         get_valid_urls(url)
      else:
         for data in user_data["data"]["children"]:
            if "permalink" in data["data"]:
               print "\n"+data["data"]["permalink"]
               new_url = "http://www.reddit.com"+data["data"]["permalink"]+"/.json?limit=500"
               if old_url != new_url:
                  depth += 1
                  get_threads_from_users(new_url)
                  depth -= 1
   except UnicodeEncodeError:
      pass


# Main function which calls the above two functions
def get_threads_from_users(url):
   global depth
   global old_url
   global user_names
   global num_retries
   global num_threads
   global thread_id
   global current_comment
   global num_comments
   try:
      filename = wget.download(url.encode('ascii','ignore'), "tmp/testing.json")
      thread  = json.load(open(filename))
      if "error" in thread:
         time.sleep(5)
         num_retries+=1
         if num_retries > 2:
            num_retries = 0
            return
         get_threads_from_users(url)
      else:
         user_csv = open("users.csv", 'a')              
         user_writer = csv.writer(user_csv)
         num_threads += 1
         thread_id = 'T'
         thread_id = thread_id+str(num_threads)
         user_writer.writerow( [thread_id] )
         user_csv.close()
         print "\n"+thread_id
         num_comments += 1
         current_comment = 'C'+str(num_comments)
         parse_thread_for_users(thread[1], thread[0]["data"]["children"][0]["data"]["author"], current_comment)
         if depth <= max_depth:
            for child in thread[1]["data"]["children"]:
               if "author" in child["data"] and child["data"]["author"] != "[deleted]":
                  author_name = child["data"]["author"]
                  print "\n"+author_name
                  old_url = url;
                  new_url = "http://www.reddit.com/user/"+author_name+"/.json"
                  get_valid_urls(new_url)
      #open("updated-parsedjson.json", "w").write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
   except UnicodeEncodeError:
      pass

# All the threads which have been chosen for now.
get_threads_from_users("http://www.reddit.com/r/IAmA/comments/4n5r3s/hi_im_jerry_seinfeld_and_welcome_to_my_third_ama/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/56gt8f/sean_hannitys_defense_of_trump_is_now_beyond/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/worldnews/comments/59rq4b/president_vladimir_putin_on_thursday_accused/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/movies/comments/59rggi/shane_black_says_the_success_of_deadpool_has_made/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/sports/comments/59nezj/the_perfect_freekick/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/news/comments/59o4cm/texas_school_district_spends_12m_in_surplus_money/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/worldnews/comments/5avwdv/uk_government_must_consult_parliament_before/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5avwrg/emails_show_how_republicans_lobbied_to_limit/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5av0ct/dear_america_please_dont_vote_for_donald_trump/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5auarb/gary_johnson_donald_trump_will_be_in_court_over/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5as0av/cuban_id_rather_lose_every_penny_than_have_trump/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5aruyn/trump_childrape_accuser_to_speak_today/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5auarb/gary_johnson_donald_trump_will_be_in_court_over/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5aw9s5/no_you_cant_text_your_vote_but_these_fake_ads/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5ax67a/i_am_gloria_la_riva_the_socialist_candidate_for/.json?limit=500")

#second round
depth = 0
get_threads_from_users("https://www.reddit.com/r/worldnews/comments/5exz2e/fidel_castro_is_dead_at_90/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/gifs/comments/5ez1r8/black_friday_madness_in_canada/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/politics/comments/5ezdd4/gop_politician_who_sexted_teen_boy_says_hes_not/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/pics/comments/5ezttv/every_thanksgiving_my_little_cousin_challenges_me/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/videos/comments/5ez31h/tom_hanks_doing_the_forrest_gump_voice_20_years/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/OldSchoolCool/comments/5exrbq/my_grandpa_back_in_mexico_1953_and_the_day_he_got/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/funny/comments/5ezsil/this_is_what_happens_when_nice_countries_fight/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/creepy/comments/5ezm6r/always_test_the_water_before_swimming_in/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/AskReddit/comments/5ez3tg/what_did_your_parents_almost_name_you/.json?limit=500")
depth = 0
get_threads_from_users("https://np.reddit.com/r/atheism/comments/5eobxq/meet_your_new_a_secretary_of_education/dae5zrx/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/gaming/comments/5f00q2/my_dad_and_uncle_having_a_doom_lan_match_in_the/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/gaming/comments/5f0kdj/close_but_no_cigar/.json?limit=500")
depth = 0
get_threads_from_users("https://www.reddit.com/r/gaming/comments/5eyakc/just_in_case_you_wondered_how_amazing_google/.json?limit=500")


print "\nNUM THREADS : "
print num_threads
'''
csv_file = open("users.csv", 'a')              
writer = csv.writer(csv_file)
for user in user_names:
   writer.writerow( [user] )
csv_file.close()
'''

# Output the updated file with pretty JSON                                      
#open("updated-parsedjson.json", "w").write(
#    json.dumps(thread, sort_keys=True, indent=4, separators=(',', ': ')))
