import matplotlib.pyplot as plt 

temperature = []
temperature_set = []
time = []
i = 0
with open("plot_data.txt") as f:
    for line in f:
        if line[-1] == '\n':
            line = line[:-1].split()
        if float(line[1]) == 27.00: 
            time.append(i)
            temperature.append(float(line[0]))
            temperature_set.append(float(line[1]))
        i+=1

plt.plot(time, temperature, label='Temperatura Rzeczywista')
plt.plot(time, temperature_set, label='Temperatura Zadana')
plt.xlabel('Czas (s)')
plt.ylabel('Temperatura (°C)')
plt.title('System Regulacji Temperatury')
plt.grid()
plt.legend()
plt.savefig("Charakterystyka.png")
plt.show()