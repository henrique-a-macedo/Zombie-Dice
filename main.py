"""

Aluno: Henrique Aguiar Macedo
Projeto: Zombie Dice
Curso: Análise e Tecnologia em Desenvolvimento de Sistemas
Matéria: Raciocínio Computacional
Turma: 01


NOTA: Eu fiz as variáveis e diversas coisas em inglês pela prática. Os textos das strings eu coloquei em português para melhor entendimento durante execução.
"""

import os
import random

#region variavéis e listas
#region Variáveis players
players = []
current_player = ''
#endregion

#region informação dos dados

dice_colors = {

'Green': ('BRAIN', 'BRAIN', 'BRAIN', 'STEPS', 'STEPS', 'SHOTGUN'),
'Yellow': ('BRAIN', 'BRAIN', 'STEPS', 'STEPS', 'SHOTGUN', 'SHOTGUN'),
'Red': ('BRAIN', 'STEPS', 'STEPS', 'SHOTGUN', 'SHOTGUN', 'SHOTGUN')
    
}

#endregion
#endregion

class Game:
    """Essa é a classe para o funcionamento do jogo em si."""

    def __init__(self): #metodo inicial
        self.players = players
        self.highest_score = 0
        self.winners = []
        self.players_game()
        self.turn_loop()
   
    def win(self,player):
        """ metodo de mandar a mensagem caso alguém ganhe o jogo"""
        print(f'O jogo acabou e o ganhador é:', player.name.upper())
        print('')  

    def turn_loop(self):
        """ metodo pra rodar o turno dos jogadores, um while que atualiza o score para o highest score para calcular quem ganha (13+ cérebros)"""
        while True:
            for player in self.players:
                
                player.player_round()

                if player.score > self.highest_score:
                    self.highest_score = player.score
                pass

                if player.score >= 13:
                    self.winners.append(player)
            print('')
            
            for player in self.players:
                
                print('O jogador', player.name.upper(), 'tem', player.score, 'ponto(s).')
            
            print('')
            print('=' * 50)
            print('')
            
            if len(self.winners) > 1:
                print(f'Os ', len(self.winners), ' jogadores ', self.winners, ' empataram.')
                break

            elif len(self.winners) == 1:
                self.win(self.winners[0])
                break

        self.game_end()

    def players_game(self): 
        """metodo para definir o número de jogadores com error handling para o número ser uma int"""
        print('Bem vindo ao jogo Zombie Dice! \n\nRegras: O jogo é bem simples, ele deve conter 2 ou mais pessoas. Cada jogador irá ter um turno por vez. O turno consiste em pegar 3 dados do tubo de dados, rolar e verificar as faces. Caso caia a face CÉREBRO ou TIRO, o jogador deixará o dado a sua frente. Caso caia a face PASSOS, o jogador pode optar por jogar novamente com este dado mais X dados do tubo, onde X é 3 - o número de passos, ou seja, o jogador sempre deve rolar 3 dados por vez, se tiver a face passos ele usará 1 passo e pegará 2 dados do tubo. Quando o jogador acumular 3 faces de tiros a sua frente, ele descarta todos os dados de cérebros acumulados e perde a vez. Após o jogador jogar os 3 primeiros dados, ele pode optar por jogar novamente(até acabar os dados do tubo), ou parar e contabilizar os pontos(faces de cérebros). O primeiro jogador a obter 13 pontos, na rodada, vence.')
        print('')

        number_of_players = 0

        while number_of_players < 2:

            try: 
                number_of_players = int(input('Digite o número de jogadores: '))
            
                if number_of_players < 2:
                    print('O número de jogadores precisa ser 2 ou mais.')

                for player in range(number_of_players):

                    player_name = input('Digite o nome do jogador ' + str(player + 1) + ': ')
                    new_player = Player(player_name)
                    players.append(new_player)
                    print('')

            except ValueError:
                print('Favor colocar um número corretamente.')

        print('=' * 50)
        print('Vamos ao jogo!!')
        print('=' * 50)
        current_player = players[0]

    def game_end(self):
        """Metodo para quando a condição de vitoria ser executada (chamada para reiniciar o jogo ou fechar a aplicação)."""
        input('Pressione enter para continuar.')
        input('')
        ge = input('Você quer reiniciar a partida? Digite "S" para sim ou qualquer outra coisa para não.').upper()
        if ge == 'S':
            self.restart()
        else:
            quit()

    def restart(self):
        """Metodo que é chamado quando a condição de reiniciar a partida é executada."""
        self.players = players
        self.highest_score = 0
        self.winners = []
        self.players_game()
        self.turn_loop()
        
class Player:
    """Essa é a classe para o controlador do jogador, todas informações dos jogadores ficarão contidas aqui."""

    pool_dados = ['Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Red', 'Red', 'Red'] #lista contendo os dados

    def __init__ (self, name):
        """Metodo inicial com os atributos necessários para os jogadores."""
        self.name = name
        self.hand = []
        self.pool_dados = ['Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Red', 'Red', 'Red']
        self.score = 0
        self.dices = 0
        self.round_faces = {
            'BRAIN': 0,
            'STEPS': 0,
            'SHOTGUN': 0
        }
        self.table = []

    def __repr__ (self):
        """Metodo de representação (nome dos jogadores)"""
        return self.name    
    
    def get_dices(self):
        """metodo para pegar os dados do tubo com um for que escolhe aleatoriamente da lista, adiciona a uma variavel chamda dice, coloca na mão do jogador e adiciona um contador para o número de dados ja jogados nesse turno."""

        for i in range(3 - len(self.hand)): 
            roll = random.randrange(len(self.pool_dados))
            dice = Dice(self.pool_dados.pop(roll))
            self.hand.append(dice)
            self.dices += 1
            
        print('Você já pegou:', self.dices,'dados')    
        
    def throw_dice(self):
        """Metodo para rolar os dados, escolher as faces(face_roll), adicionar as faces atuais e informar para o jogador qual a cor e a face que caiu."""         
        print('-' * 50)
        for dice in self.hand:
            face_roll = dice.face_roll()             
            self.round_faces[face_roll] += 1
            print('A cor do dado é:',dice.color.lower(),'e a face é:',dice.side.lower())
            
        print('-' * 50)

    def return_dices(self):
        """Metodo para retornar os dados para o tubo e resetar as faces dos jogadores no turno."""
        self.hand = []
        self.pool_dados = ['Green', 'Green', 'Green', 'Green', 'Green', 'Green', 'Yellow', 'Yellow', 'Yellow', 'Yellow', 'Red', 'Red', 'Red']
        self.round_faces = {
            'BRAIN': 0,
            'STEPS': 0,
            'SHOTGUN': 0
        }
        self.dices = 0


    def return_continue_dices(self):
        """Metodo para retornar os dados para o tubo e continuar jogando."""
        for dice in self.table:
            if (dice.side == 'BRAIN'):
                dice.reset_side()
                self.pool_dados.append(dice.color)
                self.table.remove(dice)

    def player_round(self):
        """Metodo que controla o turno do jogador, informa a quantidade de pontos, tiros e cérebros da rodada."""
        print('O jogador atual é o:',self.name.upper())
        print('')
        print('Você já tem', self.score, 'ponto(s).')
        print('')

        while True:  #Condição para o turno do jogador, onde ele precisa ter 3 dados para jogar. #TODO
            roundOk = self.get_dices()

            if not roundOk: #Caso não haja dados suficientes no tubo, o turno é encerrado automaticamente e os pontos armazenados
                print('Você já pegou todos os dados possíveis e não há 3 dados o suficientes para uma nova jogada.')
                print('Você pegou',self.round_faces['BRAIN'], 'cérebro(s).')
                self.return_continue_dices()
                print('=' * 50)

            self.throw_dice()
           
            if self.round_faces['SHOTGUN'] >= 3: #caso o jogador role 3 "tiros", ele perde a vez automaticamente e retorna os dados para o tubo
                print('Você morreu (Tomou 3 tiros)! Perca a vez.')
                self.return_dices()
                print('=' * 50)
                break

            print(f'Nessa rodada você já tem', self.round_faces['BRAIN'],'cérebro(s).\n')
            print(f'Você já tomou', self.round_faces['SHOTGUN'],'tiro(s).\n')

            resp = input('Você deseja continuar jogando? "S" para sim ou qualquer outra letra para não. ').upper()
            print('')



            if resp == 'S': #logica para remover as faces que não são passos da mão para não re rolar esses dados
                handcopy = self.hand.copy()
                for dice in handcopy:
                    if (dice.side == 'BRAIN' or dice.side == 'SHOTGUN'):
                        self.table.append(dice)
                        self.hand.remove(dice)
                # print('-' * 50)

            else:
                self.score += self.round_faces['BRAIN']
                print('Você pegou',self.round_faces['BRAIN'], 'cérebro(s).')

                #Return Dices
                self.return_dices()
                print('=' * 50)
                break
              
class Dice:

    def __init__(self, color):
        """Método par definir o dado"""
        self.color = color
        self.side = None

    def __repr__(self):
        """Metodo de representação"""
        if self.side != None:
            return f'Cor: {self.color} - Face: {self.side}'
        return f'Cor: {self.color}'

    def face_roll(self):
        """Metodo para escolher aleatoriamente a face do dado pela cor"""
        self.side = random.choice(dice_colors[self.color])
        return self.side

    def reset_side(self):
        """Resetar o lado do dado."""
        self.side = None

Game() #iniciar o jogo  