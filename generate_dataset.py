import math
import os
import random, json
import copy,re
import pandas as pd
import numpy as np
from collections import Counter



def init_user(user_profile, dream_dress_id):
    """
    :param user_profile: patience, exigence, etc?
    :return: init_S_u
    """
    visual_attrs = ['Belt', 'Color', 'Hem Shaped', 'Length', 'Neckline', 'Pattern Type',
                    'Sleeve Length', 'Sleeve Type', 'Style', 'Type', 'Waist Line']

    hidden_attrs = ['Care Instructions', 'Chest Pad','Composition','Fabric', 'Fit Type','Material'] # price

    dream_dress_info = pd.read_csv('dream_dress_info.csv')

    C_u_0 = []
    for c in visual_attrs:
        cand = dream_dress_info[c][dream_dress_info['id']==dream_dress_id].values[0]
        # p = re.compile('[/,]')
        # # print(cand)
        # cands = re.split(p,cand)
        # if '/' in cand:
        #     print(cands)
        # cands = [c for c in cands if c and c!='None']
        if cand and cand != "None":
            # value = random.choice(cand)
            C_u_0.append((c, cand))

    R_u_0 = []
    for r in hidden_attrs:
        R_u_0.append((r,""))

    if user_profile["exigence"]:
        n = random.randint(5, 10)
        m = random.randint(2,4)
    else:
        n = random.randint(2, 5)
        m = random.randint(0,2)
    C_u_0 = random.sample(C_u_0, min(n,len(C_u_0)))
    R_u_0 = random.sample(R_u_0, min(m,len(R_u_0)))

    R_u_0 = [("price", "")]+R_u_0



    A_u_0 = []
    buy = random.randint(0, 1)
    a_buy = ("buy", buy, "bye")
    A_u_0.append(a_buy)
    A_u_0 += [("request", r[0], r[1]) for r in R_u_0]
    A_u_0 += [("inform", c[0], c[1]) for c in C_u_0]

    return C_u_0, R_u_0, A_u_0

class User():
    def __init__(self,dream_dress_id,user_profile):
        # self.user_profile = {"patience": patience, "exigence": exigence, "take_advise": take_advise}
        self.user_profile = user_profile
        # print(self.user_profile)
        self.C,self.R,self.A = init_user(self.user_profile, dream_dress_id)
        self.C_total = copy.copy(self.C)
        self.response_body = None
        self.doing_action = None
        self.must_c = copy.copy(random.choice(self.C))
        self.df_dress_info = pd.read_csv("dress_info.csv")
        self.final_decision = [self.A.copy()[0]]
        # print(self.final_decision)

    def _find_answer(self, idx, attr_name):
        return self.df_dress_info[attr_name][self.df_dress_info["id"] == idx].values[0]

    def _dealwith_C(self):
        if self.user_profile['patience']:
            n = random.randint(1, 2)
        else:
            n = random.randint(min(2, len(self.C)), min(4, len(self.C)))
        if n > len(self.C):
            n = len(self.C)
        # print(self.A[-n:])
        self.response_body = copy.copy(self.A[-n:])
        self.doing_action = 'inform'
        self.A = self.A[:-n]
        self.C = self.C[:-n] # ff就想这么写！

    def _dealwith_R(self,product_id):
        if self.user_profile['patience']:
            n = 1
        else:
            n = random.randint(min(2, len(self.R)), min(3, len(self.R)))


        self.response_body = copy.copy([(i[0],i[1],product_id) for i in self.A[-n:]])
        self.doing_action = 'request'
        self.A = self.A[:-n]
        self.R = self.R[:-n]

    def deal_action(self,system_action,system_body):
        if self.A==[]:
            self.response_body = self.final_decision
            self.doing_action = 'bye'

        elif system_action == 'greeting':
            self._dealwith_C()

        elif system_action == 'request':
            if system_body[0][0] == 'not_satisfaction':
                if not self.user_profile['take_advise']:

                    self.response_body = [("must_c", self.must_c[0], self.must_c[1])]
                    self.doing_action = 'inform'

                    self.A = self.A[:-len(self.C)] if len(self.C) >0 else self.A
                    self.C = []
                    return
                # si les candidats trouvés sont déjà insatisfaisants; l'user doit arrêter de poser les conditions
                if len(self.C) != 0:
                    self.A = self.A[:-len(self.C)] # when len(C)=0, self.A[:-0] is empty rather than self.A[:-1]
                    self.C = []
            elif system_body[0][0] == 'must_c':
                pass
            else:
                for idx in system_body[0][2]:
                    for C_remove in [remove_data for remove_data in self.C_total if remove_data not in self.C]:

                        if not set(self._find_answer(idx,C_remove[0]).split(',')).intersection(set(C_remove[1].split(','))):
                            # print(idx) # sys found wrong pieces
                            self.response_body = [("negate", C_remove[0], C_remove[1])]
                            self.doing_action = 'inform'
                            return

                if not self.user_profile['take_advise']:
                    if random.uniform(0, 1) > 0.9:
                        self.response_body = [("change", system_body[0][1], system_body[0][2])]
                        self.doing_action = 'inform'
                        return

            if len(self.C)>0:
                self._dealwith_C()

            elif len(self.R) >0:
                product_id = random.choice(system_body[0][2])
                self._dealwith_R(product_id)
            else:
                print('error')

        elif system_action == 'find':
            if len(self.R) >0:
                self._dealwith_R(system_body[0][0])
            else:
                self.response_body = self.final_decision
                self.doing_action = 'bye'



def init_system():
    C_s_0 = []
    R_s_0 = []
    A_s_0 = [("greeting", "", "")]

    return C_s_0, R_s_0, A_s_0


class System():
    def __init__(self,sys_profile):
        self.system_profile = sys_profile
        # print(self.system_profile)
        self.C,self.R,self.A = init_system()
        self.request_body =None
        self.doing_action = None

        self.df_dress_info = pd.read_csv("dress_info.csv")
        # self.C = []

    def search_single(self, attr_name, attr_value):
        # Todo: other categories

        if type(attr_value) == str:

            if attr_name != 'Color':
                candidates_ids = self.df_dress_info['id'][(self.df_dress_info[attr_name].str.contains(attr_value)) & ((self.df_dress_info[attr_name].str.contains(",")) | (self.df_dress_info[attr_name].str.contains("/")))]
                candidates_exs = self.df_dress_info['id'][(self.df_dress_info[attr_name] == attr_value) & ((~self.df_dress_info[attr_name].str.contains(",")) | (~self.df_dress_info[attr_name].str.contains("/")))]
                candidates_ids = set(candidates_ids).union(set(candidates_exs))
            else: # User ask for Pink, "Dusty Pink" is also correct
                candidates_ids = self.df_dress_info['id'][(self.df_dress_info[attr_name].str.contains(attr_value))]

        else:
            candidates_ids = self.df_dress_info['id'][self.df_dress_info[attr_name] == attr_value]
        return candidates_ids

    def search_in_db(self,user_body,remove_candidate=None):
        # Todo: smarter way to combine search_single and search_in_db
        candidates_all_ids = []
        ## make mistake
        with open("dress_attr_value.json", "r") as rf:
            dictionary = json.load(rf)
            # here the values are single, no combination
        if random.uniform(0, 1) > self.system_profile['smart'] and user_body[0][0] not in ['must_c','negate','change']:
            # print("System made a stupid mistake.")
            lucky_one= random.choice(user_body)

            index = [index for index in range(len(self.C)) if self.C[index][1] == lucky_one[1]][0]
            # lucky = random.choice(C)
            # it's possible that user asks for a combination value like "bishop sleeve, drop shoulder"
            # print("User wanted at begining "+str(self.C[index][2]))
            # print("Mistake attr_name is "+str(self.C[index][1]))

            p = re.compile('[/,]')
            for v in re.split(p,self.C[index][2]):
                dictionary[self.C[index][1]] = [mm for mm in dictionary[self.C[index][1]] if mm !=v]
            dictionary[self.C[index][1]] = [mm for mm in dictionary[self.C[index][1]] if mm != self.C[index][2]]
            result = random.choice([r for r in dictionary[self.C[index][1]] if r not in self.C[index][2]])

            self.C[index] = (self.C[index][0],self.C[index][1],result)
            # print("Mistake result is "+str(result))
            self.A.append(("Mistake",self.C[index][1],result))
            self.system_profile['smart'] = math.log2(self.system_profile['smart'] + 1)

        if user_body[0][0] == 'must_c':
            temp_candidates = []
            candidates_must_ids = []
            for c in self.C:
                attr_name = c[1]
                attr_values = c[2]
                p = re.compile('[/,]')
                for attr_value in re.split(p, attr_values):
                    if attr_name != user_body[0][1]: # attrs that are not "must_c"
                        candidates_ids = list(self.search_single(attr_name, attr_value))
                        temp_candidates.append(candidates_ids)

            attr_name_must, attr_values_must = user_body[0][1], user_body[0][2]
            p = re.compile('[/,]')
            for attr_value_must in re.split(p, attr_values_must):
                cands_must_ids = list(self.search_single(attr_name_must, attr_value_must))
                candidates_must_ids.append(cands_must_ids)

            candidates_must_ids = [item for sublist in candidates_must_ids for item in sublist]
            # temp_candidates = [item for sublist in temp_candidates for item in sublist]

            for sublist in temp_candidates:
                ## 取must的交集的数据
                candidates_all_ids.append(list(set.intersection(*map(set, [candidates_must_ids,sublist]))))
                # print("======", candidates_all_ids)
            flat_all = [item for sublist in candidates_all_ids for item in sublist]
            # print("***********",flat_all)
            if not flat_all: #no intersection of must_c and other conditions, then just give must_ids
                candidates_final_ids = candidates_must_ids
            else:
                count = Counter(flat_all)
                candidates_final_ids = sorted(count.keys(), key=count.get, reverse=True)[:5]
            is_satisfied = True
            self.A.append(("Must_c",))
        else: # normal situation
            for c in self.C:
                attr_name = c[1]
                attr_values = c[2]
                p = re.compile('[/,]')
                for attr_value in re.split(p,attr_values):
                    candidates_ids = list(self.search_single(attr_name, attr_value))
                    candidates_all_ids.append(candidates_ids)
            candidates_final_ids = set.intersection(*map(set, candidates_all_ids))
            if not candidates_final_ids:
                flat_all = [item for sublist in candidates_all_ids for item in sublist]
                count = Counter(flat_all)
                candidates_final_ids = sorted(count.keys(), key=count.get, reverse=True)[:5]
                is_satisfied = False
                if len(candidates_final_ids)==0:
                    print("Nothing found in database.")
                # print("No item match all your constraints, but these ones fit the most : {}".format(candidates_final_ids))
            else:
                if remove_candidate:
                    for remove_tmp in remove_candidate:
                        if remove_tmp in candidates_final_ids:
                            candidates_final_ids.remove(remove_tmp)
                    if len(candidates_final_ids)==0:
                        is_satisfied = False
                        candidates_final_ids =remove_candidate
                    else:
                        is_satisfied = True
                        candidates_final_ids = random.sample(candidates_final_ids, min(len(candidates_final_ids),5))
                else:
                    candidates_final_ids = random.sample(candidates_final_ids, min(len(candidates_final_ids),5))
                    is_satisfied = True
            # print("These are some ones we've found for you : {}".format(candidates_final_ids))
        # Todo: img
        # candidates_final_img = self.df_product_attrs['']
        return candidates_final_ids,is_satisfied

    # Todo: when we find, we should know the productID, should add a function to locate the product ID
    def _find_answer(self, idx, attr_name):
        return self.df_dress_info[attr_name][self.df_dress_info["id"] == idx].values[0]

    def deal_action(self,user_action,user_body):
        if user_action == 'greeting':
            # print(self.A)
            self.doing_action = 'greeting'
            self.request_body = self.A
            self.A = []

        elif user_action == 'inform':
            # if user_body[0][0] == 'must_c':
            #     self.C = user_body
            if user_body[0][0] == 'negate':
                for i in range(len(self.C)):
                    c=self.C[i]
                    if c[1]==user_body[0][1]:
                        c=(c[0],c[1],user_body[0][2])
                        # print("Corrected wrong"+str(user_body[0][2]))
                        self.C[i]=c
                # print(self.C)
            elif user_body[0][0] == 'must_c':
                pass
            elif user_body[0][0] == 'change':
                candidates_final_ids, is_satisfied = self.search_in_db(user_body,user_body[0][2])
                self.doing_action = 'request'
                if is_satisfied:
                    self.request_body = [('changed', 'image', candidates_final_ids)]
                else:
                    self.request_body = [('not_satisfaction', 'image', candidates_final_ids)]
                self.A.extend(self.request_body)
                return
            else:
                self.C.extend(user_body)

            candidates_final_ids,is_satisfied =self.search_in_db(user_body)
            # print(candidates_final_ids)
            self.doing_action = 'request'
            if is_satisfied:
                if user_body[0][0]=='must_c':
                    self.request_body = [('must_c', 'image', candidates_final_ids)]
                else:
                    self.request_body = [('request','image',candidates_final_ids)]
            else:
                self.request_body = [('not_satisfaction', 'image', candidates_final_ids)]
            self.A.extend(self.request_body)


        elif user_action == 'request':
            self.request_body = []
            for i in user_body:
                r = (i[2],i[1],self._find_answer(i[2],i[1]))
                self.request_body.append(r)
                self.R.append(r)
            self.doing_action = 'find'
            self.A.extend(self.request_body)

        elif user_action == 'bye':
            self.doing_action = 'bye'
            self.request_body = [('bye','','')]
            self.A.extend(self.request_body)


def templating(attr, value, speaker, action, df_templates, category="dress", together=False):
    if speaker == 'system':
        if action=='answer':
            if attr in ["Care Instructions", "Composition", "Fit Type", "Material", "Fabric", "price"]:
                cands = df_templates["Sys template"][df_templates["attr"] == attr].values[0]
                p = re.compile("(?<=[;.]) ")
                candidates = re.split(p, cands.strip())
                say = random.choice(candidates)
                if attr == "Composition":
                    value = value.replace(",", " and")
                say = re.sub("@value@", value, say)
                say = re.sub("@attr@", attr, say)
                say = re.sub("@category@", category, say)

            elif attr == "Chest Pad":
                if value in ['None', np.NAN, 'none']:
                    say = "I'm sorry I don't see any specific information of it."
                elif value in ["Yes", "yes"]:
                    say = value
                else:
                    say = "No, it doesn't have any."


    elif speaker == 'user':
        if action == "request":
            cands = df_templates["User template"][df_templates["attr"] == attr].values[0]
            p = re.compile("(?<=[;.?]) ")
            candidates = re.split(p, cands.strip())
            say = random.choice(candidates)
            say = re.sub("@category@", category, say)
            say = re.sub("@attr@", attr, say)
            # if attr == 'Care Instructions':
            #     print(say)
            # say = re.sub("@value@", value, say)

        elif action == 'inform':
            if attr == "Belt":
                if value == "Yes":
                    say = "@category@ with @attr@, "
                else:
                    say = "@category@ without @attr@, "

            elif attr == "Sleeve Length":
                if value not in ['Sleeveless','Cap sleeve, Sleeveless']:
                    say = "@category@ with @value@, "
                elif value == 'Sleeveless':
                    candidates = ["@category@ which is @value@, ", "@value@ @category@, "]
                    say = random.choice(candidates)
                else:
                    say = "@category@ which has Cap Sleeve or is Sleeveless, "
            else:
                value = value.replace(","," or")
                cands = df_templates["User template"][df_templates["attr"]==attr].values[0]
                p = re.compile("(?<=[;.?]) ")
                candidates = re.split(p, cands.strip())
                say = random.choice(candidates)

            if together==True:
                return say # return list that's enough

            say = re.sub("@category@", category, say)
            say = re.sub("@attr@", attr, say)
            say = re.sub("@value@",value,say)
            say = say.replace("Hem Shaped", "Shape Hem")
            say = say.replace("neck neckline", "neck")
            say = say.replace("neck Neckline", "neck")
            say = say.replace("Pattern Type","Pattern")
            say = say.replace("waist waist line", "waist line")

    return say

def paraphrase(locuteur,slots,df_templates,category='dress'):
    # when together, len slots >1, slots[0][0] == 'inform', all slots are "inform"
    # We paraphrase all the demands of "inform" together rather than seperated
    if slots[0][0]=='inform':
        says_with = []
        says_adj = []
        says_which = []
        for s in slots:
            attr, value = s[1], s[2]
            if s[2] == 'None':
                value = 'no matter what'
            say = templating(attr=attr, value=value, action='inform', speaker=locuteur, df_templates=df_templates,
                             together=True)
            say = re.sub("@attr@", attr, say)
            say = re.sub("@value@", value, say)
            if any(x in say for x in ["with"," of "," in "]) :
                says_with.append(say)
            elif "which " in say:
                says_which.append(say)
            else:
                says_adj.append(say)

        # adj cat + adj cat = adj, adj cat
        if len(says_adj) > 1:
            says_adj = [s.replace('@category@', '') for s in says_adj[:-1]] + [says_adj[-1]]
        # says_adj = ''.join(says_adj)

        # dress with pockets, with long sleeves
        if says_adj:
            says_with = [s.replace('@category@', '') for s in says_with]
            # says_with = [says_with[0]]+[s.replace('with', '') for s in says_with[1:]]
        else:
            if len(says_with) > 1:
                says_with = [says_with[0]] + [s.replace('@category@', '') for s in says_with[1:]]
        # says_with = ''.join(says_with)

        if any([says_adj, says_with]):
            says_which = [s.replace('@category@', '') for s in says_which]
        else:
            says_which = [says_which[0]] + [s.replace('@category@', '') for s in says_which[1:]]
        # says_which = ''.join(says_which)

        says = says_adj + says_with + says_which
        if len(says) > 1:
            if len(says)==2:
                says_final = ' '.join(says)
            else:
                says_final = ' '.join(says[:-1]) + ' and ' + says[-1]
        elif len(says) == 1:
            says_final = says[0]
        else:
            says_final = ''
            print("Error inform together, no output.")

        says_final = re.sub("@category@", category, says_final)

        says_final = says_final.replace("Hem Shaped", "Shape Hem")
        says_final = says_final.replace("neck neckline", "neck")
        says_final = says_final.replace("neck Neckline", "neck")
        says_final = says_final.replace("Pattern Type", "Pattern")
        says_final = says_final.replace("waist waist line", "waist line")

        prefix = ["I want to find a ", "I would like to find a ", "I want to buy a ", "I'm looking for a "]
        says_final = random.choice(prefix) + says_final
        says_final = says_final.replace("  "," ")
        for x in [",;",", ;",", .",",.","; .",";.",",",", "]:
            if says_final.endswith(x):
                says_final = says_final[:-len(x)]+"."
        says_final = says_final.replace(",;", ",")
        says_final = says_final.replace(", ;", ",")
        says_final = says_final.replace(", and", " and")
        # says_final = says_final.replace(", with", " with")
        says_final = says_final.replace(", of", " of")
        says_final = says_final.replace(",; with", ", with")
        says_final = says_final.replace(", ; with", ", with")
        says_final = says_final.replace(" ,", ",")
        return [says_final]
    else:
        return interpret(locuteur,slots,df_templates)


def interpret(locuteur,slots,df_templates,category='dress'):
    '''

    :param
    - locuteur: user
    - slots: [('inform', 'Type', 'Pinafore')]
    :return: (half natural language): I want a Pinafore type dress
    '''
    utterance = []
    if locuteur=='user':
        for s in slots:
            say = ''
            if s[0] == 'inform':
                attr,value=s[1],s[2]
                if s[2]=='None':
                    value='no matter what'
                # candidates = []
                # candidates.append("I want to find a {} {} dress.".format(value,s[1]))
                # candidates.append("I would like to find a dress with {} kind of {}.".format(value,s[1]))
                # candidates.append("I want to buy a dress with {} {}.".format(value, s[1]))
                # say = random.choice(candidates)
                say = templating(attr=attr,value=value,action='inform',speaker=locuteur,df_templates=df_templates)
                prefix = ["I want to find a ","I would like to find a ","I want to buy a ","I'm looking for a "]
                say = random.choice(prefix)+say

            elif s[0] == 'must_c':
                say = "In fact, I just care about the {} of the piece, I want it to be {} and that'll be fine.".format(s[1],s[2])
            elif s[0] == 'request':
                # candidates = []
                # candidates.append("I want to know the {} of dress {}.".format(s[1], s[2]))
                # candidates.append("What is the {} of dress {} ?".format(s[1], s[2]))
                # candidates.append("Could you tell me what {} is {} ?".format(s[2], s[1]))
                # say = random.choice(candidates)
                dress_id = s[2]
                value = ''
                say = templating(attr=s[1],value=value,action='request',speaker=locuteur,df_templates=df_templates)
                # if s[1] == 'Care Instructions':
                #     print(say)
                # send the image to the system as its id
            elif s[0] == 'change':
                candidates = ["Do you have any other option?","More options?","Maybe you have some other pieces than these?","I don't want these, maybe you could show me some other options?"]
                say = random.choice(candidates)

            elif s[0] == "negate":
                candidates = ["No, these are not what I want.", "Oh, I think you are wrong with it.","No I don't want this."]
                say = templating(attr=s[1],value=s[2],action='inform',speaker=locuteur,df_templates=df_templates)
                prefix = " I want a "
                suffix = " not these."
                say = random.choice(candidates)+prefix+say+suffix

            elif s[0] == 'buy':
                if s[1]==1:
                    say = "Ok I'll buy it, bye-bye."
                else:
                    say = "Ok I'll check out it another time, thanks for your help, bye."
            if say.endswith(","):
                say = say[:-1] + "."
            if say:
                utterance.append(say)
            else:
                print("No utterance generated", s)


    elif locuteur == 'system':
        for s in slots:
            say = ''
            if s[0]=='greeting':
                say = "Hello, may I help you?"

            elif s[0]=='request':
                candidates = []
                candidates.append("I've found something interesting for you. Here are some of them {}.".format(s[2]))
                candidates.append("Here are some products that meet your demands : {}.".format(s[2]))
                candidates.append("Ok, here's some propositions. {} Do you wanna choose one of these dresses? ".format(s[2]))
                candidates.append("Do you like anyone of these dresses? {}".format(s[2]))
                say = random.choice(candidates)

            elif s[0]=='bye':
                say = "Thank you for all, looking forward to seeing you again."

            elif s[0]=='must_c':
                say = "Ok, got it. Then how about these dresses? {} They fit your demands as many as possible.".format(s[2])

            elif s[0]=='not_satisfaction':
                say = "There's no item that can match all your demands, but these ones fit the most : {}".format(s[2])

            elif s[0]=='changed':
                candidates = []
                candidates.append("I've found some other pieces for you. Here are some of them {}.".format(s[2]))
                candidates.append("Here are some other pieces that might interest you : {}.".format(s[2]))
                candidates.append(
                    "Ok then, here's some other propositions. {} Do you wanna choose one of these items? ".format(s[2]))
                candidates.append("No problem. Do you like anyone of these dresses? {}".format(s[2]))
                say = random.choice(candidates)
            else: # (2303164, 'price', 'US$11.36')
                # candidates = []
                # candidates.append("The {} of dress {} is {}".format(s[1],s[0],s[2]))
                # candidates.append("Dress {}'s {} is {}".format(s[0],s[1],s[2]))
                # say = random.choice(candidates)
                attr, value = s[1], s[2]
                say = templating(attr=attr,value=value,speaker=locuteur,action="answer",df_templates=df_templates)
            if say.endswith(","):
                say = say[:-1] + "."
            if say:
                utterance.append(say)
            else:
                print("No utterance generated", s)
    return utterance


def make_dialog(version_dir,dream_dress_id, user_id, sys_id, v):
    '''

    :param dream_dress_id: int
    :param user_id,sys_id: int
    :param user_profile: dict(patience=True, exigence=True,take_advise=False)
    :param sys_profile: dict(sale=True,smart=0.9)
    TODO sale=True的话，system要稍微介绍一下某个产品
    :return: json_file
    '''
    with open('user_persona.json','r') as ur, open('sys_persona.json','r') as sr:
        users = json.load(ur)
        systems = json.load(sr)
        # user,sys=None,None

        for u in users:
            if u['user_id']==user_id:
                user_profile = u['user_profile']
        for s in systems:
            if s['sys_id']==sys_id:
                sys_profile = s['sys_profile']

    df_templates = pd.read_csv("dress_attrs_templates.csv")

    with open(version_dir+"_o/"+str(dream_dress_id)+'_'+str(user_id)+'_'+str(sys_id)+'_'+str(v)+".json",'w') as w,\
         open(version_dir+"_x/"+str(dream_dress_id)+'_'+str(user_id)+'_'+str(sys_id)+'_'+str(v)+".json",'w') as wx:
        content = []
        content_x = []
        User1 = User(dream_dress_id, user_profile)
        System1 = System(sys_profile)
        content.append({'user_id':user_id,'user_profile':copy.copy(user_profile),'dream_id':dream_dress_id,'user_C0':copy.copy(User1.C)})
        content.append({'sys_id':sys_id,'sys_profile':copy.copy(sys_profile)})

        content_x.append({'user_id': user_id, 'user_profile': copy.copy(user_profile),'user_C0':copy.copy(User1.C)})
        content_x.append({'sys_id': sys_id, 'sys_profile': copy.copy(sys_profile)})


        dialogue = []
        dialogue_x = []

        System1.deal_action('greeting', None)
        dialogue.append({"turn_id": 0,
                         "system_action": copy.copy(System1.request_body),
                         "system_utterance": interpret("system", System1.request_body,df_templates)})
        dialogue_x.append({"turn_id": 0,
                         "system_action": copy.copy(System1.request_body),
                         "system_utterance": interpret("system", System1.request_body,df_templates)})
        i = 1
        while i < 15:
            # print("system", copy.copy(System1.request_body))
            User1.deal_action(System1.doing_action, System1.request_body)
            # print('user', copy.copy(User1.response_body))
            System1.deal_action(User1.doing_action, User1.response_body)
            dialogue.append({"turn_id": i,
                             "user_action": copy.copy(User1.response_body),
                             "user_utterance": interpret('user', User1.response_body,df_templates),
                             "user_utterance_para":paraphrase('user',User1.response_body,df_templates),
                             "system_action": copy.copy(System1.request_body),
                             "system_utterance": interpret("system", System1.request_body,df_templates)})
            dialogue_x.append({"turn_id": i,
                             "user_action": copy.copy(User1.response_body),
                             "user_C": copy.copy(User1.C),
                             "user_R": copy.copy(User1.R),
                             "user_A": copy.copy(User1.A),
                             "user_utterance": interpret('user', User1.response_body,df_templates),
                             "user_utterance_para": paraphrase('user', User1.response_body, df_templates),
                             "system_action": copy.copy(System1.request_body),
                             "system_C": copy.copy(System1.C),
                             "system_R": copy.copy(System1.R),
                             "system_A": copy.copy(System1.A),
                             "system_utterance": interpret("system", System1.request_body,df_templates)})
            if System1.request_body[0][0] == 'bye':
                break

            i += 1

        content.append(dialogue)
        content_x.append(dialogue_x)
        json.dump(content,w)
        json.dump(content_x,wx)


if __name__ == '__main__':
    # import shutil
    # shutil.rmtree('dialog_v0_para_o')
    # shutil.rmtree('dialog_v0_para_x')
    # os.mkdir('dialog_v0_para_o')
    # os.mkdir('dialog_v0_para_x')
    from tqdm import tqdm
    with open("dream_dresses.json",'r') as r:
        dream_ids = json.load(r)
    print(len(dream_ids))
    stupid_sid = [0,1,2,3,4,5,6,10,11,12,13,14,15,16]
    clever_sid = [7,8,9,17,18,19]
    # for v in range(10):
    #     make_dialog('dialog_v0',2988675,1,0,v)
    #     print('')

    for did in tqdm(dream_ids):
        for uid in tqdm(range(8),desc="User",leave=False):
            for sid in tqdm(stupid_sid,desc="Stupid System",leave=False):
                for v in range(1):
                    try:
                        make_dialog('dialog_v0_para', did, uid, sid, v)
                    except Exception as e:
                        print("======={}=============".format((did, uid, sid, v)))
                        print('error is %s'%(str(e)))

            for sid in tqdm(clever_sid,desc="Clever System",leave=False):
                for v in range(3):
                    try:
                        make_dialog('dialog_v0_para', did, uid, sid, v)
                    except Exception as e:
                        print("======={}=============".format((did, uid, sid, v)))
                        print('error is %s' % (str(e)))
