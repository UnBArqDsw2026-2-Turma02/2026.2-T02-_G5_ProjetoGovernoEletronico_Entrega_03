package recursoslai;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

public class InterfaceRecursosLAI extends JFrame {
    private final JTextField protocolo = new JTextField("REC-0099", 18);
    private final JTextField cidadao = new JTextField("Cidadão de Teste", 18);
    private final JCheckBox tempestivo = new JCheckBox("Recurso dentro do prazo de 10 dias", true);
    private final JCheckBox executivoFederal = new JCheckBox("Órgão do Poder Executivo Federal", true);

    private final JComboBox<String> decisao1 = new JComboBox<>(new String[] {"Manter negativa (encaminhar)", "Deferir"});
    private final JComboBox<String> decisao2 = new JComboBox<>(new String[] {"Manter negativa (encaminhar)", "Deferir"});
    private final JComboBox<String> decisaoCGU = new JComboBox<>(new String[] {"Manter negativa (encaminhar)", "Deferir"});
    private final JComboBox<String> decisaoCMRI = new JComboBox<>(new String[] {"Indeferir (encerrar)", "Deferir"});
    private final JTextArea saida = new JTextArea(18, 72);

    public InterfaceRecursosLAI() {
        super("Informa.BR — Recursos da LAI | Chain of Responsibility");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setMinimumSize(new Dimension(850, 680));
        setLocationByPlatform(true);

        JPanel formulario = new JPanel(new GridBagLayout());
        formulario.setBorder(BorderFactory.createTitledBorder("Dados do recurso e decisões simuladas"));
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(5, 8, 5, 8);
        c.anchor = GridBagConstraints.WEST;
        c.fill = GridBagConstraints.HORIZONTAL;

        int row = 0;
        adicionarLinha(formulario, c, row++, "Protocolo:", protocolo);
        adicionarLinha(formulario, c, row++, "Nome do cidadão:", cidadao);
        adicionarLinha(formulario, c, row++, "Tempestividade:", tempestivo);
        adicionarLinha(formulario, c, row++, "Vínculo do órgão:", executivoFederal);
        adicionarLinha(formulario, c, row++, "1ª instância — autoridade hierárquica superior:", decisao1);
        adicionarLinha(formulario, c, row++, "2ª instância — autoridade máxima do órgão:", decisao2);
        adicionarLinha(formulario, c, row++, "3ª instância — CGU:", decisaoCGU);
        adicionarLinha(formulario, c, row++, "4ª instância — CMRI:", decisaoCMRI);

        tempestivo.addActionListener(e -> atualizarDisponibilidade());
        executivoFederal.addActionListener(e -> atualizarDisponibilidade());

        JButton executar = new JButton("Processar recurso");
        executar.addActionListener(e -> processarRecurso());
        JButton limpar = new JButton("Limpar resultado");
        limpar.addActionListener(e -> {
            saida.setText("");
        });
        JPanel botoes = new JPanel();
        botoes.add(executar);
        botoes.add(limpar);

        saida.setEditable(false);
        saida.setLineWrap(true);
        saida.setWrapStyleWord(true);
        saida.setFont(new java.awt.Font(java.awt.Font.MONOSPACED, java.awt.Font.PLAIN, 12));
        JScrollPane scroll = new JScrollPane(saida);
        scroll.setBorder(BorderFactory.createTitledBorder("Cadeia percorrida e resultado"));

        JLabel nota = new JLabel("As opções simulam as respostas das instâncias; a cadeia Java determina quais handlers são acionados.");
        JPanel inferior = new JPanel(new BorderLayout(6, 6));
        inferior.add(botoes, BorderLayout.NORTH);
        inferior.add(scroll, BorderLayout.CENTER);
        inferior.add(nota, BorderLayout.SOUTH);

        setLayout(new BorderLayout(8, 8));
        add(formulario, BorderLayout.NORTH);
        add(inferior, BorderLayout.CENTER);
        ((JPanel) getContentPane()).setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));
        atualizarDisponibilidade();
    }

    private void adicionarLinha(JPanel painel, GridBagConstraints c, int linha, String rotulo, java.awt.Component componente) {
        c.gridy = linha;
        c.gridx = 0;
        c.weightx = 0;
        painel.add(new JLabel(rotulo), c);
        c.gridx = 1;
        c.weightx = 1;
        painel.add(componente, c);
    }

    private void atualizarDisponibilidade() {
        boolean ativo = tempestivo.isSelected();
        decisao1.setEnabled(ativo);
        decisao2.setEnabled(ativo);
        decisaoCGU.setEnabled(ativo && executivoFederal.isSelected());
        decisaoCMRI.setEnabled(ativo);
    }

    private void processarRecurso() {
        String id = protocolo.getText().trim();
        String nome = cidadao.getText().trim();
        if (id.isEmpty() || nome.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Preencha o protocolo e o nome do cidadão.", "Dados obrigatórios", JOptionPane.WARNING_MESSAGE);
            return;
        }

        Recurso recurso = new Recurso(id, nome, tempestivo.isSelected(), executivoFederal.isSelected());
        InstanciaHandler cadeia = new ValidadorTempestividadeHandler();
        cadeia.encadear(new AutoridadeHierarquicaSuperiorHandler(selecionadoDeferir(decisao1)))
              .encadear(new AutoridadeMaximaOrgaoHandler(selecionadoDeferir(decisao2)))
              .encadear(new CGUHandler(selecionadoDeferir(decisaoCGU)))
              .encadear(new CMRIHandler(decisaoCMRI.getSelectedIndex() == 1));

        StringBuilder relatorio = new StringBuilder();
        relatorio.append("=== PROCESSAMENTO DO RECURSO ===\n");
        relatorio.append("Protocolo: ").append(id).append('\n');
        relatorio.append("Cidadão: ").append(nome).append('\n');
        relatorio.append("Tempestivo: ").append(simNao(tempestivo.isSelected())).append('\n');
        relatorio.append("Órgão do Executivo Federal: ").append(simNao(executivoFederal.isSelected())).append("\n\n");
        relatorio.append("--- Log da cadeia de handlers ---\n");

        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        try (PrintStream captura = new PrintStream(buffer, true, StandardCharsets.UTF_8.name())) {
            System.setOut(captura);
            cadeia.handle(recurso);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Não foi possível processar o recurso: " + ex.getMessage(), "Erro", JOptionPane.ERROR_MESSAGE);
            return;
        } finally {
            System.setOut(original);
        }

        relatorio.append(new String(buffer.toByteArray(), StandardCharsets.UTF_8));
        relatorio.append("\n--- RESULTADO FINAL ---\n");
        relatorio.append("Status: ").append(recurso.getStatus()).append('\n');
        relatorio.append("Instância responsável: ")
                 .append(recurso.getInstanciaResponsavelPelaDecisao() == null ? "—" : recurso.getInstanciaResponsavelPelaDecisao())
                 .append('\n');
        relatorio.append("Motivo: ")
                 .append(recurso.getMotivoDaDecisao() == null ? "—" : recurso.getMotivoDaDecisao())
                 .append('\n');
        saida.setText(relatorio.toString());
        saida.setCaretPosition(0);
    }

    private boolean selecionadoDeferir(JComboBox<String> combo) {
        return combo.getSelectedIndex() == 1;
    }

    private String simNao(boolean valor) {
        return valor ? "Sim" : "Não";
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new InterfaceRecursosLAI().setVisible(true));
    }
}
