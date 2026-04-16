import cv2
import numpy as np

# Spesifiser input- og output-filer her
navn = "trans5"  # Endre til ønsket navn for både input og output, uten filendelse
inn_navn = f"Nye_videoer/{navn}"   
ut_navn = f"{navn}"

filename = f"/Users/tordtranum/Desktop/6.semester/Sensorer/Lab/Lab_3_Optikk/Txt_målinger/Videoer/{inn_navn}.mp4"  # Endre til ønsket videofil
output_filename = f"/Users/tordtranum/Desktop/6.semester/Sensorer/Lab/Lab_3_Optikk/Txt_målinger/{ut_navn}"  # Endre til ønsket output-fil

# Les videoen
cap = cv2.VideoCapture(filename, cv2.CAP_FFMPEG)
if not cap.isOpened():
    print("Kunne ikke åpne inputfilen. Feil filnavn, eller OpenCV-pakken din er kanskje ikke bygget med FFMPEG-støtte.")
    exit()

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

mean_signal = np.zeros((num_frames, 3))

# Loop gjennom videoen
count = 0
ROI = None  # Initialiser ROI
while cap.isOpened():
    ret, frame = cap.read()  # 'frame' er en numpy-array med dimensjoner [høyde, bredde, 3], i rekkefølge BGR
    if not ret:
        break

    # Vis vindu for valg av ROI
    if count == 0:
        window_text = 'Velg ROI ved å dra musen, og trykk SPACE eller ENTER når du er fornøyd.'
        ROI = cv2.selectROI(window_text, frame, fromCenter=False, showCrosshair=True)  # ROI inneholder: [x, y, w, h] for valgt rektangel
        cv2.destroyWindow(window_text)
        if ROI[2] == 0 or ROI[3] == 0:  # Sjekk om ROI er gyldig
            print("Ugyldig ROI valgt. Avslutter.")
            exit()
        print("Looper gjennom videoen.")

    # Beregn gjennomsnitt
    cropped_frame = frame[ROI[1]:ROI[1] + ROI[3], ROI[0]:ROI[0] + ROI[2], :]
    if cropped_frame.size == 0:  # Sjekk om det er et gyldig område
        print(f"Tomt område valgt i frame {count}.")
        mean_signal[count, :] = [np.nan, np.nan, np.nan]
    else:
        mean_signal[count, :] = np.mean(cropped_frame, axis=(0, 1))
    count += 1

cap.release()

# Fjern eventuelle tomme rader (dersom videoen har færre frames enn forventet)
mean_signal = mean_signal[:count, :]

# Lagre til fil i rekkefølge R, G, B
np.savetxt(output_filename, np.flip(mean_signal, 1))
print(f"Data lagret til '{output_filename}', fps = {fps} bilder/sekund")