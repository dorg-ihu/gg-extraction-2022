from re import compile, sub, findall, search, escape, DOTALL, match
from collections import OrderedDict
from gg18.ggHelper import Helper
from gg18.respAclassifier import paragraphClf
from src.fek_parser import FekParser

class RespaExtractor(object):
    
    def __init__(self, txtpath, text):
    		self.standard_paorg_detect_accuracy = 0.65
    		self.acronym_paorg_detect_accuracy = 0.85
    		self.__illegal_chars = compile(r"\d+")
    		##################################################
    		## Το be constantly expanded (lots of variants) ##
    		##################################################
    		self.issue_number_key = "Αρ. Φύλλου"
    		self.issue_type_keys = ["ΑΠΟΦΑΣ", "ΠΡΟΕΔΡΙΚ", "[ΝN][OΟ][ΜM][OΟ]", "ΚΑΝΟΝΙΣΜ", "ΠΡΑΞ", "ΠΡΟΚΗΡΥΞ"]
    		self.dec_contents_key = "ΠΕΡΙΕΧΟΜΕΝΑ\nΑΠΟΦΑΣΕΙΣ"
    		self.decs_key = "ΑΠΟΦΑΣΕΙΣ"
    		self.summaries_start_keys = ["ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ\’ ΑΡΙΘ[^\n]+", "KANOΝΙΣΜΟΣ ΥΠ\’ ΑΡΙΘ[^\n]+", "ΝΟΜΟΣ ΥΠ\’ ΑΡΙΘ[^\n]+", 
    									 "[^«]ΠΡΑΞΗ ΝΟΜΟΘΕΤΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ[^\n]+"]
    		self.dec_prereq_keys = ["χοντας υπόψη:", "χοντας υπόψη", "χοντες υπόψη:", "χουσα υπόψη:", "χουσα υπ’ όψει:", "χοντας υπόψη του:", 
    								"χοντας υπ\' όψη:", "χοντας υπ\’ όψη:", "Αφού έλαβε υπόψη:", "Λαμβάνοντας υπόψη:"]
    		self.dec_init_keys = ["αποφασίζουμε:", "αποφασίζουμε τα ακόλουθα:", "αποφασίζουμε τα εξής:", "διαπιστώνεται:",
    							  "αποφασίζει:", "αποφασίζει τα ακόλουθα:", "αποφασίζει τα εξής:", "αποφασίζει ομόφωνα:",
    							  "αποφασίζει ομόφωνα και εγκρίνει:", "αποφασίζει τα κάτωθι", "αποφασίζεται:", "ψηφίζει:",
    							  "με τα παρακάτω στοιχεία:"]
    		self.dec_end_keys = {'start_group': ["Η απόφαση αυτή", "Ηαπόφαση αυτή", "Η απόφαση", "Η περίληψη αυτή", 
    											 "η παρούσα ισχύει", "Η παρούσα απόφαση", "Η ισχύς του παρόντος", 
    											 "Ο παρών Κανονισμός", "Η ισχύς της παρούσας", "Η ισχύς των διατάξεων"],
    							 'finish_group': ["την δημοσίευση", "τη δημοσίευση", "τη δημοσίευσή", "να δημοσιευθεί", "να δημοσιευτεί", "να δημοσιευθούν",  
    											 "F\n", "της δημοσιεύσεώς", "δημοσίευση", "θα κυρωθεί"]}
    		self.respa_keys = {'assignment_verbs':["ναθέτουμε", "νατίθεται", "νατίθενται", "νάθεση", "ρίζουμε", "παλλάσσουμε", "εταβιβάζουμε"], 
    						   'assignment_types':["αθήκοντ", "ρμοδιότητ", "αθηκόντ", "ρμοδιοτήτ"]}
    
    		self.paorg_unit_keys = ["Τμήμα", "Διεύθυνση", "Υπηρεσία"]
    		self.dec_correction_keys = ['Διόρθωση', 'ΔΙΌΡΘΩΣΗ']
    		self.article_keys = ["Άρθρο"]
    		self.last_article_keys = ["Έναρξη Ισχύος", "Έναρξη ισχύος", "Η ισχύς του παρόντος", "EΝΑΡΞΗ ΙΣΧΥΟΣ"]
    		self.fekParser = FekParser(txtpath)
    		self.text = text
    		return
    
    def get_dec_prereqs(self):
    		"""
			Return dictionary (or list if txt is peculiar) of the prerequisites 
			of each decision.
				
			@param txt: GG Issue containing decisions

			e.g.
			{
				1: 	(Έχοντας υπόψη:)
					"1. Τις διατάξεις του άρθρου 280 παρ. Ι του ν.3852/2010, 
					«Νέα Αρχιτεκτονική της Αυτοδιοίκησης και της Αποκε-
					ντρωμένης Διοίκησης - Πρόγραμμα Καλλικράτης».
					2. ... "(αποφασίζουμε:)

				2:  (Έχοντας υπόψη:)
					"1. Τις διατάξεις του άρθρου 58 του ν.3852/2010 (Φ.Ε.Κ. 
					87/Α΄) «Νέα Αρχιτεκτονική της Αυτοδιοίκησης και της 
					Αποκεντρωμένης Διοίκησης - Πρόγραμμα Καλλικράτης».
					2. ... "(αποφασίζουμε:)
				...
			}

			@TODO:
			1. Generalize for different issues
			"""
    		txt = Helper.clean_up_txt(self.txt)
    		
    		dec_prereq_keys = self.dec_prereq_keys
    		dec_init_keys = self.dec_init_keys
    
    		dec_prereqs = {}
    		prereq_bodies = findall(r"(?:{})(.+?)(?:{})".format(Helper.get_special_regex_disjunction(dec_prereq_keys),
    															Helper.get_special_regex_disjunction(dec_init_keys)),
    															txt, flags=DOTALL)
    		if prereq_bodies:
    			# Place into dict
    			for dec_idx in range(len(prereq_bodies)):
    				dec_prereqs[dec_idx + 1] = prereq_bodies[dec_idx]
    		else: 
    			# Find whatever seems like prereqs
    			dec_prereqs = findall(r"\.\n[Α-ΩΆ-ΏA-Z](.+?)(?:{})".format(Helper.get_special_regex_disjunction(dec_init_keys)), 
    																	txt, flags=DOTALL)
    			
    		return dec_prereqs
    
    
    def get_articles(self):
    	""" 
    		Return a dictionary of articles contained within a GG Issue.
    		
    		@param txt: GG Issue containing articles

    		e.g. 
    		{
    			1: 'Άρθρο 1\nΑποστολή \nΤο Υπουργείο Ανάπτυξης και Ανταγωνιστικότητας 
    				\nέχει ως αποστολή τη διαμόρφωση της αναπτυξιακής \nπολιτικής της χώρας 
    				που στοχεύει στην προώθηση ...'
    			2: 'Άρθρο 2\nΔΙΑΡΘΡΩΣΗ ΥΠΗΡΕΣΙΩΝ\nΟι υπηρεσίες του Υπουργείου, διαρθρώνονται ως εξής:\n
    				1. α. Πολιτικά Γραφεία Υπουργού και Υφυπουργών\nβ. Γραφεία Γενικών Γραμματέων\nγ. 
    				Γραφείο Ειδικού Γραμματέα\nδ. Αυτοτελές Τμήμα Εσωτερικού Ελέγχου\nε. ...'
    			...
    		} 
    	"""
    	articles = []
    	if self.txt: 
    		articles = findall(r"({artcl}\s*\d+\s*\n.+?)(?={artcl}\s*\d+\s*\n)"\
    						.format(artcl=self.article_keys[0]), self.txt, flags=DOTALL)
    		last_article = findall(r"({artcl}\s*\d+\s*\n(?:{last_article}).+?\.\s*\n)"\
    						.format(artcl=self.article_keys[0], 
    								last_article=Helper.get_special_regex_disjunction(self.last_article_keys)), 
    						self.txt, flags=DOTALL)
    		
    		if last_article:
    			assert(len(last_article) >= 1)
    			articles.append(last_article[0])
    		return dict(zip(range(1, len(articles) + 1), articles))
    
    
    def get_paragraphs(self):
    	text = Helper.clean_up_txt(self.txt)
    	text = Helper.remove_txt_prelims(text)
    	# txt = Helper.codify_list_points(txt)
    	paragraphs = []
    	if text:
    		paragraphs = findall(r"\n?\s*([Ά-ΏΑ-Ωα-ωά-ώBullet\d+\(•\-\−]+[\.\)α-ω ][\s\S]+?(?:[\.\:](?=\s*\n)|\,(?=\s*\n(?:[α-ω\d]+[\.\)]|Bullet))))", text)
    	return paragraphs
    
    
    def get_units_and_respas_following_respas_decl(self):
    		"""  
    			Return a dictionary of rough Organization Unit - RespA associations
    			mentioned as a RespA declaration followed by a Unit-RespAs list.
    			
    			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
    										  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
    												Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
    												Θρησκευμάτων.",
    
    												"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
    												Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
    												τισμού." etc.
    
    			e.g.
    			{
    				"Τμήμα Διαχείρισης και Ανάπτυξης Ανθρώπινου Δυναμικού Τομέα Εμπορίου Καταναλωτή και Βιομηχανίας": [
    			        "β. Τμήμα Διαχείρισης και Ανάπτυξης Ανθρώπινου Δυναμικού Τομέα Εμπορίου−Καταναλωτή και Βιομηχανίας.",
    			        "αα. Η εφαρμογή της κείμενης νομοθεσίας που αφορά στην υπηρεσιακή κατάσταση και στις υπηρεσιακές \nμεταβολές του πάσης φύσεως προσωπικού.",
    			        "ββ. Η κατανομή των οργανικών θέσεων, η περιγραφή \nκαι ανάλυση των καθηκόντων καθώς και ο καθορισμός \nτων περιγραμμάτων εργασίας\nγγ. Η καταγραφή των υπηρεσιακών αναγκών και η \nστελέχωση (διορισμοί−τοποθετήσεις−μετακινήσεις, αποσπάσεις, μετατάξεις) για την κάλυψη αυτών.",
    			        "δδ. Η στελέχωση των Πολιτικών Γραφείων του Υφυπουργού και των Γενικών ή Ειδικών Γραμματέων του \nΤομέα.",
    			        "εε. Η έκδοση αποφάσεων για μετακινήσεις εκτός \nέδρας στο εσωτερικό και στο εξωτερικό για εκτέλεση \nυπηρεσίας υπαλλήλων.",
    			        "στστ. Η παρακολούθηση και εφαρμογή της κινητικότητας των υπαλλήλων.",
    			        "ζζ. Η αριθμητική καταγραφή και παρακολούθηση του \nπάσης φύσεως προσωπικού και η διαρκής ενημέρωση \nτου Μητρώου Μισθοδοτούμενων καθώς και η σύνταξη \nκαταστάσεων με στοιχεία του προσωπικού (επετηρίδα) \nκαι η τήρηση των προσωπικών μητρώων των υπηρετούντων υπαλλήλων.",
    			        "ηη. Η χορήγηση των πάσης φύσεως αδειών.",
    			        "θθ. Η διαδικασία έγκρισης υπερωριών του πάσης φύσεως προσωπικού.",
    			        "ιι. Η ηλεκτρονική θεώρηση βιβλιαρίων ιατροφαρμακευτικής περίθαλψης των υπαλλήλων.",
    			        "ιαια. Η εφαρμογή των διατάξεων περί αξιολόγησης \nπροσωπικού.",
    			        "ιβιβ. Η εφαρμογή των διατάξεων περί καθορισμού των \nετήσιων στόχων και δεικτών μέτρησης αποδοτικότητας \nκαι αποτελεσματικότητας, η παρακολούθηση υλοποίησης και η αναθεώρησή τους καθώς και η σύνταξη της \nετήσιας έκθεσης απολογισμού και επί μέρους εκθέσεων \nαξιολογήσεων/μετρήσεων για τις Υπηρεσιακές Μονάδες.",
    			        "ιγιγ. Η καταγραφή των αναγκών εκπαίδευσης και επιμόρφωσης του στελεχιακού δυναμικού, η κατάρτιση \nτου ετήσιου εκπαιδευτικού προγράμματος καθώς και \nη διαχείριση μητρώου εκπαιδευθέντων.",
    			        "ιδιδ. Η εφαρμογή του πειθαρχικού δικαίου και των διατάξεων περί αργίας−αναστολής εκτέλεσης καθηκόντων."
    			    ],
    			    "Τμήμα Διοικητικής Υποστήριξης Οργάνωσης και Τεχνικών Υπηρεσιών του Τομέα Ανάπτυξης": [
    			        "α. Τμήμα Διοικητικής Υποστήριξης, Οργάνωσης και \nΤεχνικών Υπηρεσιών του Τομέα Ανάπτυξης.",
    			        "αα. Η μέριμνα για την τήρηση του ωραρίου μέσω των \nκαρτών προσέλευσης−αναχώρησης του προσωπικού.",
    			        "ββ. Η τήρηση του Γενικού Πρωτοκόλλου (φυσικού ή \nκαι ηλεκτρονικού) του Τομέα.",
    			        "γγ. Η διεκπεραίωση της απλής και διαβαθμισμένης \nαλληλογραφίας και του λοιπού έντυπου και ηλεκτρονικού υλικού.",
    			        "δδ. Η επικύρωση αντιγράφων, εγγράφων και η βεβαίωση του γνησίου της υπογραφής, σύμφωνα με το 1 του Ν. 4250/2014 (Α΄ 74).",
    			        "εε. Η επίδοση εγγράφων και λοιπού έντυπου υλικού \nεντός και εκτός του Τομέα.",
    			        "στστ. Η ευθύνη για τις διαδικασίες αναπαραγωγής \nζζ. Η ευθύνη για την κίνηση των υπηρεσιακών οχηεγγράφων.",
    			        "μάτων.\nηη. Οι ενέργειες για τη χωροταξική κατανομή και στέγαση των Υπηρεσιών του Υπουργείου σε συνάρτηση με \nτο αντικείμενό τους και την εξυπηρέτηση του πολίτη \nκαθώς και η μέριμνα για την ορθολογική διαχείριση και \nεξοικονόμηση ενέργειας στα κτίρια του Υπουργείου.",
    			        "θθ. Η ευθύνη για την ομαλή λειτουργία των τηλεφωνικών κέντρων.",
    			        "ιι. Η υλοποίηση, επίβλεψη και συντονισμός των διαδικασιών για τη συντήρηση, βελτίωση, φύλαξη και \nπυρασφάλεια των χώρων και των εγκαταστάσεων, τη \nφροντίδα για την καθαριότητα των καταστημάτων του \nΥπουργείου καθώς και τη λειτουργία των FAX, μέσων \nεπικοινωνίας και των φωτοτυπικών μηχανημάτων.",
    			        "ιαια. Οι μελέτες και προτάσεις προς το Τμήμα Κατάρτισης και Εκτέλεσης Προγράμματος Προμηθειών για \nτην προμήθεια υλικού και εξοπλισμού της Κεντρικής \nΥπηρεσίας καθώς και για κάθε είδους προμήθειες που \nαφορούν τον Τομέα, όπως επίσης και ο προγραμματισμός για τεχνικά έργα.",
    			        "ιβιβ. Η διενέργεια της επίβλεψης−καταμέτρησηςπαραλαβής τεχνικών εργασιών σε συνεργασία με τη Διεύθυνση Προμηθειών, Υποδομών και Διαχείρισης Υλικού \nτου Υπουργείου.",
    			        "ιγιγ. Η λειτουργία και εφαρμογή των σύγχρονων εργαλείων διαχείρισης των Βιβλιοθηκών, η διασύνδεση και \nανταπόκριση στα αιτήματα των εργαζομένων.",
    			        "ιδιδ. Η ευθύνη της μελέτης, υπόδειξης και παρακολούθησης εφαρμογής μέτρων για την απλούστευση \nγραφειοκρατικών τύπων και την καθιέρωση προσφορότερων μεθόδων εργασίας για την αύξηση της παραγωγικότητας.",
    			        "ιειε. Η εξυπηρέτηση−πληροφόρηση του πολίτη.",
    			        "ιστιστ. Η εξασφάλιση της προσβασιμότητας και λοιπών διευκολύνσεων για τα άτομα με αναπηρίες στους \nχώρους λειτουργίας του Υπουργείου."
    			    ],
    			}
    		"""
    		paragraph_clf = paragraphClf()
    		#articles_as_paragraphs = self.fekParser.articles_as_paragraphs
    		articles = self.fekParser.articles
    		units_and_respas_following_respas_decl = OrderedDict()
    		units_threshold = 100
    		respas_threshold = 60
    		
    		def set_units_and_respas_following_respas_decl_dict(paragraphs):
    			respas_decl_criteria = False
    			# paragraphs = list(map(lambda prgrph: prgrph.replace('Bullet ', ''), paragraphs))
    			for i, prgrph in enumerate(paragraphs):
    				prgrph_has_respas_decl = paragraph_clf.has_respas_decl(prgrph[:300])
    				first_list_elem_has_unit = paragraph_clf.has_units(paragraphs[i+1]) if (i + 1) < len(paragraphs) else False
    				respas_decl_criteria = prgrph_has_respas_decl and first_list_elem_has_unit
    				if respas_decl_criteria:
    					j = i + 1
    					units_counter = 0
    					
    					while True:
    						break_criteria = (j >= len(paragraphs)) or (units_counter > units_threshold)
    						if break_criteria:
    							break
    						cur_prgrph = paragraphs[j]
    						respas = []
    						unit = ' '.join(Helper.get_words(Helper.remove_list_points(cur_prgrph), n=20))
    						
    						if ((paragraph_clf.has_units_and_respas(cur_prgrph) and\
    							paragraph_clf.has_units(cur_prgrph[:20])) or ('Αρμοδιότητες' in cur_prgrph and '.' not in cur_prgrph[:70])) and\
    							not Helper.contains_list_points(cur_prgrph[10:]) and\
    							(unit[0].isupper() or unit[0].isdigit()):
    							# Case 2
    							addit_prgrph = paragraphs[j+1] if j+1 < len(paragraphs) else ''
    							additional_respa_section = ('Επίσης' in addit_prgrph[:10]
    														or 'Ειδικότερα' in addit_prgrph[:10]
    														or 'Συγκεκριμένα' in addit_prgrph[:10]
    														or 'Επιπλέον' in addit_prgrph[:10]
    														or 'μήμα αυτό' in addit_prgrph[:10]
    														or 'ραφείο αυτό' in addit_prgrph[:10]) if addit_prgrph else False
    							respas = [cur_prgrph + addit_prgrph] if additional_respa_section else [cur_prgrph]
    							j += 1
    						elif paragraph_clf.has_units(cur_prgrph.replace('Αρμοδιότητες ', '')[:20]) and\
    							 unit[0].isupper():
    							# Case 1
    							for k in range(j+1, j+1+respas_threshold):	
    								# Fetch respas
    								list_bounds_ok = k < len(paragraphs)
    								if list_bounds_ok:
    									possible_respa = paragraphs[k]
    									legible_respa_criterion = (not paragraph_clf.has_units(possible_respa.replace('Αρμοδιότητες ', '')[:20]))
    									has_units_followed_by_respas = paragraph_clf.has_units_followed_by_respas(possible_respa)
    			
    									if legible_respa_criterion:
    										respa = possible_respa
    										if k == j+1:
    											# Might contain first respa
    											respas.append(cur_prgrph)
    										respas.append(respa)
    										j = k + 1
    									elif has_units_followed_by_respas and k == j + 1:
    										j = k + 1
    									else:
    										j = k
    										break
    								else:
    									j = k
    									break
    						else:
    							# Ignore
    							j += 1	
    
    						if respas:
    							
    							if unit in units_and_respas_following_respas_decl and\
    							  any([(respa not in units_and_respas_following_respas_decl[unit]) for respa in respas]):
    								units_and_respas_following_respas_decl[unit] += respas
    							else:
    								units_and_respas_following_respas_decl[unit] = respas
    
    							units_counter += 1
    			return
    	
            
        
    		 # if articles:
    		 # 	if isinstance(articles, dict): articles = list(articles.values())
    		 # 	for artcl in articles:
    		 # 		artcl_paragraphs = self.get_paragraphs(artcl)
    		 # 		set_units_and_respas_following_respas_decl_dict(artcl_paragraphs)
    		 # else:
    		 # 	paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
    		 # 	set_units_and_respas_following_respas_decl_dict(paragraphs)
    		
    		# if articles_as_paragraphs:
    		# 	for artcl in articles_as_paragraphs.values():
    		# 		artcl_paragraphs = []
    		# 		for k, v in artcl.items():
    		# 			artcl_paragraphs.append(v)
    		# 		set_units_and_respas_following_respas_decl_dict(artcl_paragraphs)
    				
    		# else:
    		# 	paragraphs = self.get_paragraphs(self.txt)
    		# 	set_units_and_respas_following_respas_decl_dict(paragraphs)
            
    		if articles:
    			if isinstance(articles, dict): articles = list(articles.values())
    			for artcl in articles:
    				artcl_paragraphs = self.fekParser.split_all(artcl)
    				set_units_and_respas_following_respas_decl_dict(artcl_paragraphs)
    		else:
    			paragraphs = self.fekParser.split_all(self.text)
    			set_units_and_respas_following_respas_decl_dict(paragraphs)
    		
    		return units_and_respas_following_respas_decl
    
    
    def get_units_followed_by_respas(self):
    		"""  
    			Return a dictionary of rough Organization Unit - RespA associations
    			mentioned as a Unit followed by a list of RespAs.
    			
    			@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
    										  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
    												Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
    												Θρησκευμάτων.",
    
    												"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
    												Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
    												τισμού." etc.
    
    			e.g.
    			{
    				"Το Τμήμα Α Προγραμματισμού και Τεκμηρίωσης είναι αρμόδιο για": [
    			        "3. Το Τμήμα Α’ Προγραμματισμού και Τεκμηρίωσης \nείναι αρμόδιο για:",
    			        "α) τη διαμόρφωση μεθοδολογικού και θεσμικού \nπλαισίου για τον εσωτερικό έλεγχο των υπηρεσιών του \nΥπουργείου και την καθοδήγηση τους για την ανάπτυξη \nσυστημάτων διαχείρισης κινδύνων,",
    			        "β) την κατάρτιση προγράμματος εσωτερικών ελέγχων \nστις Υπηρεσίες του Υπουργείου, ετήσιου ή μεγαλύτερης \nδιάρκειας, κατόπιν καθορισμού των ελεγκτέων περιοχών διαδικασιών, σε συνδυασμό με την αναγνώριση και αξιολόγηση των κινδύνων και λαμβανομένων υπόψη των \nστρατηγικών και επιχειρησιακών προτεραιοτήτων του \nΥπουργείου, συνεκτιμώντας πάσης φύσεως αναφορές, \nκαταγγελίες, εκθέσεις και κάθε άλλο στοιχείο, τηρουμένων των εκάστοτε ισχυουσών διατάξεων περί προστασίας προσωπικών δεδομένων,",
    			        "γ) την έκδοση εντολών για την διενέργεια προγραμματισμένων και έκτακτων εσωτερικών ελέγχων, όπου \nαυτό απαιτείται,",
    			        "δ) τη διασφάλιση τήρησης των Διεθνών Προτύπων και \nτων ορθών πρακτικών κατά την ελεγκτική διαδικασία, \nτην επεξεργασία των στοιχείων των επί μέρους εκθέσεων εσωτερικού ελέγχου και τη σύνταξη ετήσιας ή/\nκαι ενδιάμεσης έκθεσης, στις οποίες καταγράφονται οι \nδραστηριότητες και τα αποτελέσματα του εσωτερικού \nελέγχου,",
    			        "ε) την υποβολή της έκθεσης εσωτερικού ελέγχου στον \nοικείο Υπουργό με κοινοποίηση στις Υπηρεσίες που \nέχουν αρμοδιότητα για το σχεδιασμό και τη λειτουργία \nτου συστήματος που ελέγχθηκε και την τακτική παρακολούθηση, αξιολόγηση και επιβεβαίωση των διορθωτικών \nή προληπτικών ενεργειών που πραγματοποιούνται από \nτις υπηρεσίες σε συμμόρφωση με τις προτάσεις του εσωτερικού ελέγχου, μέχρι την οριστική υλοποίησή τους,\n στ) την εισήγηση για την κατάρτιση ή αναθεώρηση \nτου Κώδικα Δεοντολογίας Εσωτερικών Ελεγκτών και \nτην εισήγηση για την τροποποίηση του, αν αυτό κριθεί \nαναγκαίο,",
    			        "ζ) τη μέριμνα για την εκπαίδευση και την επιμόρφωση \nτων Εσωτερικών Ελεγκτών, σε συνεργασία με τις καθ΄ \nύλην αρμόδιες υπηρεσίες του Υπουργείου, καθώς και \nτην διερεύνηση και την πρόταση τρόπων ανάπτυξης των \nγνώσεων και των δεξιοτήτων τους,",
    			        "η) τον χειρισμό κάθε άλλου συναφούς θέματος."],
    			    ...
    			}
    		"""
    		paragraph_clf = paragraphClf()
    		respas_threshold = 60
    		units_followed_by_respas = OrderedDict()
    		#articles_as_paragraphs = self.fekParser.articles_as_paragraphs
    		articles = self.fekParser.articles
    		
    		def set_units_followed_by_respas_dict(paragraphs, respas_threshold):
    			appends_since_last_unit_detection = 0
    			for i, prgrph in enumerate(paragraphs):
    				
    				if paragraph_clf.has_units_followed_by_respas(prgrph) and\
    				   (Helper.remove_list_points(prgrph)[0].isdigit() or Helper.remove_list_points(prgrph)[0].isupper()):
    						
    					if sum(1 for c in prgrph[:20] if c.isupper()) <= 2 and\
    						paragraph_clf.has_only_units(Helper.remove_list_points(paragraphs[i-1])):
    						# If this paragraph has 2 or less upper characters the unit might be contained in 
    						# the previous paragraph has only units, so: add both as unit
    						prev_prgrph = paragraphs[i-1]
    						unit = prev_prgrph + ' '.join(Helper.get_words(Helper.remove_list_points(prgrph), n=20))
    					else:
    						unit = ' '.join(Helper.get_words(Helper.remove_list_points(prgrph), n=20))
    					respas = []
    					units_counter = 0
    					for j in range(i+1, i+1+respas_threshold):
    						list_bounds_ok = j < len(paragraphs)
    						if list_bounds_ok:
    							possible_respa = paragraphs[j]
    							legible_respa_criterion = (not paragraph_clf.has_units(Helper.remove_list_points(possible_respa).replace('Αρμοδιότητες ', '')[:20]))
    							if legible_respa_criterion:
    								if j == i+1:
    									# Might contain first respa
    									respas.append(paragraphs[i])
    								respas.append(possible_respa)
    								continue
    						break
    
    					if respas:
    						if unit in units_followed_by_respas and\
    						  any([(respa not in units_followed_by_respas[unit]) for respa in respas]):
    							units_followed_by_respas[unit] += respas
    						else:
    							units_followed_by_respas[unit] = respas
    
    						units_counter += 1
    			return 
    
    		# if articles:
    		# 	if isinstance(articles, dict): articles = list(articles.values())
    		# 	for artcl in articles:
    		# 		artcl_paragraphs = self.get_paragraphs(artcl)
    		# 		set_units_followed_by_respas_dict(artcl_paragraphs, respas_threshold)
    		# else:
    		# 	paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
    		# 	set_units_followed_by_respas_dict(artcl_paragraphs, respas_threshold)
    		
    		# if articles_as_paragraphs:
    		# 	for artcl in articles_as_paragraphs.values():
    		# 		artcl_paragraphs = []
    		# 		for k, v in artcl.items():
    		# 			artcl_paragraphs.append(v)
    		# 		set_units_followed_by_respas_dict(artcl_paragraphs, respas_threshold)
    				
    		# else:
    		# 	paragraphs = self.get_paragraphs(self.txt)
    		# 	set_units_followed_by_respas_dict(paragraphs, respas_threshold)
    		if articles:
    			if isinstance(articles, dict): articles = list(articles.values())
    			for artcl in articles:
    				artcl_paragraphs = self.fekParser.split_all(artcl)
    				set_units_followed_by_respas_dict(artcl_paragraphs, respas_threshold)
    		else:
    			paragraphs = self.fekParser.split_all(self.text)
    			set_units_followed_by_respas_dict(paragraphs, respas_threshold)

            
    		return units_followed_by_respas
    
    
    def get_units_and_respas(self):
    	""" 
    		Return dictionary of rough Organization Unit - RespA associations
    		mentioned in SINGLE PARAGRAPHS.
    		
    		@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
    									  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
    											Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
    											Θρησκευμάτων.",

    											"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
    											Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
    											τισμού." etc.

    		e.g. 
    		{ 
    			'Το Γραφείο Φύλαξης Πληροφόρησης είναι αρμόδιο για τον προγραμματισμό και':

    		    'Το Γραφείο Φύλαξης Πληροφόρησης είναι αρμόδιο 
    			για τον προγραμματισμό και έλεγχο της φύλαξης των 
    			Μουσείων, αποθηκών αρχαίων, αρχαιολογικών χώρων 
    			και εν γένει αρχαιολογικών εγκαταστάσεων, την τήρηση και εποπτεία της φύλαξης κατά τις ημέρες των 
    			εξαιρέσιμων και αργιών και τη σύνταξη των σχετικών 
    			καταστάσεων για την αποζημίωση των προσφερομένων 
    			υπηρεσιών κατά τις ημέρες αυτές, οι οποίες εγκρίνονται 
    			από τον Προϊστάμενο. Επιπλέον μεριμνά για την ευταξία αρχαιολογικών χώρων και μουσείων και εν γένει για 
    			την εύρυθμη λειτουργία τους, καθώς και για την ευπρεπή συμπεριφορά του αρχαιοφυλακτικού προσωπικού, 
    			όπως επίσης συντονίζει τους ορισμένους υπεύθυνους 
    			αρχιφύλακες.',
    			
    			...
    		}

    	"""
    	paragraph_clf = paragraphClf()
    	#articles_as_paragraphs = self.fekParser.articles_as_paragraphs
        #articles = self.get_articles(paorg_pres_decree_txt)
    	articles = self.fekParser.articles
    	additional_respas_threshold = 6
    	units_and_respas = OrderedDict()
    	units_and_respa_sections = []
    	
    	def get_unit_and_respa_paragraphs(paragraphs, additional_respas_threshold):
    		unit_and_respa_sections = []
    		for i, prgrph in enumerate(paragraphs):
    			unit_and_respa_paragraph_criteria = (paragraph_clf.has_units_and_respas(prgrph) or
    											  (paragraph_clf.has_units_followed_by_respas(prgrph) and len(prgrph)>150)) and\
    												paragraph_clf.has_units(prgrph.replace('Αρμοδιότητες ', '')[:20])
    			if unit_and_respa_paragraph_criteria:
    				additional_respas_following_criterion = (prgrph[-1] == ':' or prgrph[-2] == ':')
    				if additional_respas_following_criterion:
    					# Append following paragraphs 
    					# containing additional respas to prgrph
    					for j in range(i+1, i+1+additional_respas_threshold):
    						if j < len(paragraphs):
    							prgrph += paragraphs[j]
    				# Append paragraph containing unit with its respas
    				unit_and_respa_sections.append(prgrph)
    		return unit_and_respa_sections

    	def disentangle_units_from_respas(units_and_respa_sections):
    		print("units_and_respa_sections: ", unit_and_respa_sections)
    		for unit_and_respa_section in units_and_respa_sections:
    			# Unit assumed to be in 20 first words
    			unit = ' '.join(Helper.get_words(Helper.remove_list_points(unit_and_respa_section), n=20))
    			respas = unit_and_respa_section
    			# Units starts with uppercase character
    			if unit[0].isupper() or unit[0].isdigit():
    				if unit in units_and_respas and\
    				   any([(respa not in units_and_respas[unit]) for respa in respas]):
    					units_and_respas[unit] += respas
    				else:
    					units_and_respas[unit] = respas
    		return 
    				
    	# if articles:
    	# 	if isinstance(articles, dict): articles = list(articles.values())
    	# 	for artcl in articles:
    	# 		artcl_paragraphs = self.get_paragraphs(artcl)
    	# 		units_and_respa_sections.append(get_unit_and_respa_paragraphs(artcl_paragraphs, additional_respas_threshold))
    	# 	units_and_respa_sections = [item for sublist in units_and_respa_sections for item in sublist]
    	# else:
    	# 	paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
    	# 	units_and_respa_sections = get_unit_and_respa_paragraphs(paragraphs, additional_respas_threshold)
    	
    	# if articles_as_paragraphs:
    	# 	for artcl in articles_as_paragraphs.values():
    	# 		artcl_paragraphs = []
    	# 		for k, v in artcl.items():
    	# 			artcl_paragraphs.append(v)
    	# 		units_and_respa_sections.append(get_unit_and_respa_paragraphs(artcl_paragraphs, additional_respas_threshold))
    	# 	units_and_respa_sections = [item for sublist in units_and_respa_sections for item in sublist]
    	# else:
    	# 	paragraphs = self.get_paragraphs(self.txt)
    	# 	units_and_respa_sections = get_unit_and_respa_paragraphs(paragraphs, additional_respas_threshold)
    	
    	if articles:
    		if isinstance(articles, dict): articles = list(articles.values())
    		for artcl in articles:
    			artcl_paragraphs = self.fekParser.split_all(artcl)
    			units_and_respa_sections.append(get_unit_and_respa_paragraphs(artcl_paragraphs, additional_respas_threshold))
    		units_and_respa_sections = [item for sublist in units_and_respa_sections for item in sublist]
    	else:
    		#paragraphs = self.get_paragraphs(paorg_pres_decree_txt)
    		paragraphs = self.fekParser.split_all(self.text)
    		units_and_respa_sections = get_unit_and_respa_paragraphs(paragraphs, additional_respas_threshold)
    	
    	unit_and_respa_sections = [x for x in units_and_respa_sections if x]
    	disentangle_units_from_respas(units_and_respa_sections)
    	print('disentangled_units: ', unit_and_respa_sections)
    	return units_and_respas
    
    
    def get_rough_unit_respa_associations(self, format=''):
    	"""
    		Return a dictionary of rough Organization Unit - RespA associations

    		@param paorg_pres_decree_txt: GG Presidential Decree Organization Issue
    									  e.g. "ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 18 
    											Οργανισμός Υπουργείου Παιδείας, Έρευνας και 
    											Θρησκευμάτων.",

    											"ΠΡΟΕΔΡΙΚΟ ΔΙΑΤΑΓΜΑ ΥΠ’ ΑΡΙΘΜ. 4 
    											Οργανισμός Υπουργείου Πολιτισμού και Αθλη-
    											τισμού." etc.
     	"""
    	units_and_respas = self.get_units_and_respas()
    	units_followed_by_respas = self.get_units_followed_by_respas()
    	units_and_respas_following_respas_decl = self.get_units_and_respas_following_respas_decl()

    	units_and_respas.update(units_followed_by_respas)
    	units_and_respas.update(units_and_respas_following_respas_decl)
    	rough_unit_respa_associations = units_and_respas
    	
    	if format.lower() == 'json':
    		return Helper.get_json(rough_unit_respa_associations, encoding='utf-8')
    	elif format.lower() == 'xml':
    		return Helper.get_xml(rough_unit_respa_associations)
    	return rough_unit_respa_associations 
    
    
    
    
    
    
    
    
    
    
    
    
    
