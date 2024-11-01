import mysql.connector
import mysql.connector.errors

class BD:
    def __init__(self):
        self.connection = self.createConnection()

    def createConnection(self):
        print("Conectando ao banco de dados...")

        try:
            connectionBD = mysql.connector.connect(
                host="localhost",
                port="3306",
                user="root",
                password="",
                database="escola",
            )
            print("Conexão realizada com sucesso")
            return connectionBD
        except mysql.connector.errors.ProgrammingError as error:
            print("Erro de conexão", error)
            return {"error": str(error)}
        
    def login(self, nomeUsuario, senhaUsuario):
        cursor = self.connection.cursor()
        query = """
            SELECT nomeUsuario, senhaUsuario 
            FROM usuarios 
            WHERE nomeUsuario = %s AND senhaUsuario = %s
        """
        cursor.execute(query, (nomeUsuario, senhaUsuario))
        result = cursor.fetchall()
        cursor.close()

        if result:
            return {
                "nomeUsuario": result[0][0],
                "senhaUsuario": result[0][1]
            }
        else:
            return {
                "error": 'Usuário não encontrado'
            }
            
    def excluirTurma(self, codigoTurma):
        cursor = self.connection.cursor()
        try:
            query = "DELETE FROM turmas WHERE codigoTurma = %s"
            cursor.execute(query, (codigoTurma,))
            self.connection.commit() 
            cursor.close()
            return True
        
        except mysql.connector.Error as error:
            print("Erro ao excluir turma:", error)
            cursor.close()
            return False

    def buscarTurmas (self, nomeUsuario):
        cursor = self.connection.cursor()
        cursor.execute(f"select * from turmas where nomeUsuario = {nomeUsuario}")
        result = cursor.fetchall()
        turmas = {}

        if len(result) > 0:
            for i in range(len(result)):
                turmas[result[i][0]] = {
                    "codigoTurma": result[i][1],
                    "nometurma": result[i][2],
                    "periodoTurma": result[i][3]
                }
        else:
            turmas = {"error": True}

        cursor.close()
        return turmas
