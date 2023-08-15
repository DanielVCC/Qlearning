import connection as cn
import random

socket = cn.connect(2037)

def get_next_action(current_state,  epsilon):
    if random.random() < epsilon:
        #define a melhor ação a ser tomada pelo agente definida pela q_table
        index = current_state.index(max(current_state))
        print('A proxima ação será {}!'.format(actions[index]))
        return index
    else:
        #define uma ação aleatória para ser tomada pelo agente
        index = random.randint(0,2)
        print('A proxima ação será {}!'.format(actions[index]))
        return index
    
# retorna index (row) do estado
def get_state_index(binary):
    #remove os primeiros 2 caracteres '0b'
    binary = binary[2:]
    # pega os primeiros 5 bits e transforma em decimal
    platform = int(binary[:5], 2)
    # pega os 2 ultimos bits e transforma em decimal
    direction = int(binary[5:], 2)
    state = platform * 4 + direction
    return state

def get_q_value(current_state, action_index, q_table):
    return q_table[current_state][action_index]

# calcula e retorna valor de Q pra dar update na tabela
def q_update(previous_state, action_index, current_state, reward, q_table, alpha, gamma):
    previous_q_value = get_q_value(previous_state, action_index, q_table)
    estimate_q = reward + gamma * max(q_table[current_state]) # Belman
    q_value = q_table[previous_state][action_index] + alpha*(estimate_q - previous_q_value)
    return q_value

# define Q Table
f = open('resultado.txt', 'r')

q_table = []
for line in f:
    line = line[:len(line)-1] # remove a quebra de linha
    row = line.split(' ')
    row = [float(num) for num in row] # converte de str pra float
    q_table.append(row)

actions = ['left', 'right', 'jump']

epsilon = 0.4 # porcentagem de vezes que o agente tomara a melhor decisão baseada na Q table
gamma = 0.9 # variavel para equação de belman, define o peso utilidade esperado da melhor acao possivel no proximo estado
alpha = 0.25 # define o peso do novo valor calculado na equacao de belman em relacao ao historico de acoes
plataforma_inicial = 0
current_state = plataforma_inicial * 4 #inicializando o estado inical, terá que refletir o estado inicial antes do inicio do aprendizado

# inicia o aprendizado por reforço
for test in range(1000):
    action_index = get_next_action(q_table[current_state], epsilon)
    previous_state = current_state
    current_state, reward = cn.get_state_reward(socket, actions[action_index])
    current_state = get_state_index(current_state)
    print(current_state)
    print(reward)
    # calcula e faz update no valor da QTABLE
    q_table[previous_state][action_index] = q_update(previous_state, action_index, current_state, reward, q_table, alpha, gamma)

#print(q_table)

# escreve os novos Qvalues da q_table no arquivo
write_file = open("resultado.txt", "w")
for row in q_table:
     for num in range(3):
          if num != 2:
               write_file.write("{} ".format(row[num]))
          else:
               write_file.write("{}\n".format(row[2]))
          
