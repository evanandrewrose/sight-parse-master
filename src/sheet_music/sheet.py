from note import Note

class Sheet:
    def __init__(self, title, composer, beats, beat_type, clef, clef_line):
        self.title     = title
        self.composer  = composer
        self.beats     = beats
        self.beat_type = beat_type
        self.clef      = clef
        self.clef_line = clef_line
        self.notes = []
    
    #adds a note to the note list
    def add_note(self, note_object):
        self.notes.append(note_object)
        
    def export_xml(self):
        measure_number = 1
        beat_count     = 0

        #opening the file for writing
        xml_file = open("file.xml", 'w')
        
        #making a variable to control the measures
        measure_beats = ((1/float(self.beat_type)) * float(self.beats))
        
        #hardcoding the the constant values for the xml
        xml_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
        xml_file.write("<score-partwise version=\"3.0\">\n")
        xml_file.write("<work>\n")
        
        #adding the title
        xml_file.write("<work-title>")
        xml_file.write(self.title)
        xml_file.write("</work-title>\n")
        xml_file.write("</work>\n")
        xml_file.write("<identification>\n")
        xml_file.write("<creator type=\"composer\">")
        
        #adding the composer
        xml_file.write(self.composer)
        xml_file.write("</creator>\n")
        xml_file.write("</identification>\n")
        
        #adding the part list
        xml_file.write("<part-list>\n")
        xml_file.write("<score-part id=\"P1\">\n")
        xml_file.write("</score-part>\n")
        xml_file.write("</part-list>\n")
        xml_file.write("<part id=\"P1\">\n")
        
        #looping through the notes
        for i, note in enumerate(self.notes):
            #writing the measure number if there are no beats in the measure
            if beat_count == 0:
                xml_file.write("<measure number=\"")
                xml_file.write(str(measure_number))
                xml_file.write("\">\n")
                
                #adding the timing, clef, and staff lines in the first measure.
                if measure_number == 1:
                    xml_file.write("<attributes>\n")
                    xml_file.write("<divisions>1</divisions>\n")
                    xml_file.write("<key>\n")
                    xml_file.write("<fifths>0</fifths>\n")
                    xml_file.write("<mode>major</mode>\n")
                    xml_file.write("</key>\n")
                    xml_file.write("<clef>\n")
                    xml_file.write("<sign>")
                    xml_file.write(self.clef)
                    xml_file.write("</sign>\n")
                    xml_file.write("<line>")
                    xml_file.write(self.clef_line)
                    xml_file.write("</line>\n")
                    xml_file.write("</clef>\n")
                    xml_file.write("<time>\n")
                    xml_file.write("<beats>")
                    xml_file.write(self.beats)
                    xml_file.write("</beats>\n")
                    xml_file.write("<beat-type>")
                    xml_file.write(self.beat_type)
                    xml_file.write("</beat-type>\n")
                    xml_file.write("</time>\n")
                    xml_file.write("<staff-details>\n")
                    xml_file.write("<staff-lines>5</staff-lines>\n")
                    xml_file.write("<staff-tuning line=\"1\">\n")
                    xml_file.write("<tuning-step>E</tuning-step>\n")
                    xml_file.write("<tuning-octave>3</tuning-octave>\n")
                    xml_file.write("</staff-tuning>\n")
                    xml_file.write("<staff-tuning line=\"2\">\n")
                    xml_file.write("<tuning-step>G</tuning-step>\n")
                    xml_file.write("<tuning-octave>3</tuning-octave>\n")
                    xml_file.write("</staff-tuning>\n")
                    xml_file.write("<staff-tuning line=\"3\">\n")
                    xml_file.write("<tuning-step>B</tuning-step>\n")
                    xml_file.write("<tuning-octave>4</tuning-octave>\n")
                    xml_file.write("</staff-tuning>\n")
                    xml_file.write("<staff-tuning line=\"4\">\n")
                    xml_file.write("<tuning-step>D</tuning-step>\n")
                    xml_file.write("<tuning-octave>4</tuning-octave>\n")
                    xml_file.write("</staff-tuning>\n")
                    xml_file.write("<staff-tuning line=\"5\">\n")
                    xml_file.write("<tuning-step>F</tuning-step>\n")
                    xml_file.write("<tuning-octave>4</tuning-octave>\n")
                    xml_file.write("</staff-tuning>\n")
                    xml_file.write("</staff-details>\n")
                    xml_file.write("</attributes>\n")
                        
            #adding the note
            xml_file.write("<note>\n")
            xml_file.write("<pitch>\n")
            xml_file.write("<step>")
            xml_file.write(self.notes[i].value)
            xml_file.write("</step>\n")
            xml_file.write("<octave>")
            xml_file.write(self.notes[i].octave)
            xml_file.write("</octave>\n")
            xml_file.write("</pitch>\n")
            xml_file.write("<duration>")
            xml_file.write(str(self.notes[i].duration))
            xml_file.write("</duration>\n")
            xml_file.write("<type>")
            xml_file.write(self.notes[i].duration_string)
            xml_file.write("</type>\n")
            xml_file.write("</note>\n")
                
            #checking to see if new measure
            beat_count = beat_count + note.duration
            if (beat_count >= measure_beats):
                xml_file.write("</measure>\n")
                #increment the measure number
                measure_number += 1
                #since there is a new measure, reset beat count to 0
                beat_count = 0
            
            #if end of notes end the measure
            elif i == len(self.notes) - 1:
                xml_file.write("</measure>\n")

        #closing the tags       
        xml_file.write("</part>\n")
        xml_file.write("</score-partwise>\n")
        
        #closing the file 
        xml_file.close()       
        
if __name__ == "__main__":
    sheet = Sheet('Twinkle Twinkle Little Star', 'Anon', '2', '4', 'G', '2')
    
    note= Note("C", "4", .25, False)
    sheet.add_note(note)
    note= Note("C", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("A", "4", .25, False)
    sheet.add_note(note)
    note= Note("A", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("G", "4", .5, False)
    sheet.add_note(note)
    
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("D", "4", .25, False)
    sheet.add_note(note)
    note= Note("D", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("C", "4", .5, False)
    sheet.add_note(note)
    
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("D", "4", .5, False)
    sheet.add_note(note)
    
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("D", "4", .5, False)
    sheet.add_note(note)
    
    note= Note("C", "4", .25, False)
    sheet.add_note(note)
    note= Note("C", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    note= Note("G", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("A", "4", .25, False)
    sheet.add_note(note)
    note= Note("A", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("G", "4", .5, False)
    sheet.add_note(note)
    
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    note= Note("F", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    note= Note("E", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("D", "4", .25, False)
    sheet.add_note(note)
    note= Note("D", "4", .25, False)
    sheet.add_note(note)
    
    note= Note("C", "4", .5, False)
    sheet.add_note(note)

    sheet.export_xml()