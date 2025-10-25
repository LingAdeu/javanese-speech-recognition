[!header](header.png)

# **Javanese Speech Recognition Model with Whisper**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1sEv6dvIo9LjMEOZdZWB9sxWkQxKHQj0L?usp=sharing) (Model Training) 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1y4PGy9S4vR9jR7wqHLzj9ohtPujn8bR3?usp=sharing) (Model Testing)

## Summary
This project demonstrates how a speech recognition , namely Whisper was trained for Javanese language using the Whisper architecture. The model was trained and tested on [Ayush Kumar Bar](https://huggingface.co/datasets/ayush-shunyalabs/javanese-speech-dataset)'s Javanese dataset with training conducted for 3 epochs at a learning rate of 1e-5. Evaluation on 728 Javanese audio samples (syntethic or non-natural data) results in a Word Error Rate (WER) of 0.25, a Character Error Rate (CER) of 0.07, and a Real-Time Factor (RTF) of 0.06. These metrics indicate that the model achieves moderate to good transcription accuracy and with excellent performance given the low RTF (fast processing).

$$
\begin{align}
WER&=\frac{\text{Substitutions}+\text{Deletions}+\text{Insertions}}{\text{Number of Words in Reference}}\\
CER&=\frac{\text{Substitutions}+\text{Deletions}+\text{Insertions}}{\text{Number of Characters in Reference}}
\end{align}
$$

The second round of model evaluation, which was meant for a qualitative inspection, involved 75 Javanese audio samples obtained from [OpenSLR](https://www.openslr.org/41/). With this small sample size, it was found that the ASR model struggled with Javanese minimal pairs and subtle articulatory contrasts. For example,

- The model was confused with word final consonant *k* (often phonetically realized with *ʔ*) vs *h* as in \[sisɪʔ\] vs \[sisɪh\] due to the similar phonological characteristics of the sounds. Sound *ʔ* is characterized by a voiceless glottal plosive consonant whereas *h* is a voicless glottal fricative. The articuatory features of both sounds are similar in terms of voicing (voiceless) and place of articulation (glottal). Their main difference lies on the manner of articulation (how airlow is released): Sound *k* is made by firstly stopping the airflow before releasing it whereas sound *h* is created by forcing air through a narrow gap to create a hissing sound. 
- As Whisper relies on accoustic cues, the similar sounds may be confusing for the model. To investigate this further, a follow-up accoustic phonetic analysis with spectograms was done.
- The sound /o/ vs /ɔ/ (ngendhok \[ŋəndʰɔʔ\] vs ngendhog \[ŋəndʰog\]) which are in the final vowel-consonant transition may lead to confusion. (I will add a plot to show the transcription of the audio file(s) here)
- Another noticable error is the morphological reduplication as in *tutur-tuturane* and *siswa-siswane* (predicted as *tuturtuturane* and *siswasiswane*) which are used for marking plurality. Interestingly, when the reduplication comes without any suffixes as in *mugi-mugi* and *pirang-pirang*, the model correctly transcribed the audio files. This error pattern suggests that the model's confusion likely emerges from prosodic and morphological interaction. Reduplicated parts with additional suffix -e/-ne are perceived as a single continuous word with no hyphen involved. (I will add a plot to show if any clear prosodic boundary here)

## Feedback
If there are any questions or suggestions for improvements, feel free to contact me here:

<a href="https://www.linkedin.com/in/adelia-januarto/" target="_blank">
    <img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/linkedin/default.svg" width="52" height="40" alt="linkedin logo"/>
  </a>
<a href="mailto:januartoadelia@gmail.com" target="_blank">
    <img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/gmail/default.svg"  width="52" height="40" alt="gmail logo"/>
  </a>